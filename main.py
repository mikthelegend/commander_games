import gspread
from datetime import date, datetime
from google.oauth2.service_account import Credentials
import re
from deck import Deck
from game import Game

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
]

print("Authorizing credentials...")
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_id = "159wpwQBQCCreKWL2_Yh0iMy6tKPpiePRW8RVl7MnxUQ"

print("Connecting to Google Sheets...")
sheet = client.open_by_key(sheet_id)

debug = False  # Set to True to enable debug output

# Fetches all decks from the "Stats" worksheet and initializes them as Deck objects.
def get_all_decks():
    print("Fetching all decks...")
    decks = []
    for row in sheet.worksheet("Stats").get_all_values()[1:]:
        deck = Deck(*row[0:5])
        decks.append(deck)
    return decks

all_decks = get_all_decks()

def get_deck_by_name(deck_name):
    for deck in all_decks:
        if deck.name == deck_name:
            return deck
    return None

# Converts an array of deck names into a string, quoting names that contain commas.
def convert_deck_array_to_string(deck_array):
    final_string = ""
    for deck in deck_array:
        if ", " in deck:
            final_string += f'"{deck}", '
        else:
            final_string += f"{deck}, "
    return final_string[:-2]  # Remove trailing comma and space

# Fetches all games from the "Games" worksheet and returns them as a list of Game objects.
def get_all_games():
    print("Fetching all games...")
    games = []
    for row in sheet.worksheet("Games").get_all_values()[1:]:
        game = Game.from_sheet(*row[0:7])
        games.append(game)
    return games

all_games = get_all_games()

def get_all_players():
    players = set()
    for game in all_games:
        players.add(game.winner.pilot)
        for loser in game.losers:
            players.add(loser.pilot)
    return list(players)

all_players = get_all_players()

# Adds a new game to the "Games" table in the "Games" worksheet.
def add_new_game(game_id, winning_player, losing_players, winning_deck, losing_decks, date, notes):
    print(f"Adding new game with ID {game_id}...")

    date_object = datetime.strptime(date, "%Y-%m-%d").date()

    new_game = Game.verbose_init(
        game_id = game_id,
        winning_player = winning_player,
        losing_players = losing_players,
        winning_deck = winning_deck,
        losing_decks = losing_decks,
        date = f"{date_object.day}/{date_object.month}/{date_object.year % 100}",
        notes = notes
    )

    games_worksheet = sheet.worksheet("Games")
    row_data = [
        new_game.game_id,
        new_game.winner.pilot,
        ", ".join([loser.pilot for loser in new_game.losers]),
        new_game.winner.deck_name,
        convert_deck_array_to_string([loser.deck_name for loser in new_game.losers]),
        new_game.date,
        new_game.notes
    ]

    gspread_append_row(games_worksheet, row_data)

    print("New game added successfully.")

# Works around gspread's lack of support for appending rows to Table Objects by inserting a new row and shuffling the existing data down.
def gspread_append_row(worksheet, row_data):
    all_values = worksheet.get_all_values()
    last_row = len(all_values)
    next_row = last_row + 1

    worksheet.insert_row([""] * len(row_data), index=last_row) # Insert a new row at the second last position
    worksheet.update(
        f"A{last_row}:{chr(64 + len(row_data))}{last_row}", # Shuffle the last row down to the new row
        [all_values[-1]],
        value_input_option="USER_ENTERED"
    )
    worksheet.update(
        f"A{next_row}:{chr(64 + len(row_data))}{next_row}", # Overwrite the last row with the new data
        [row_data],
        value_input_option="USER_ENTERED"
    )

# Updates an existing game the "Games" table in the "Games" worksheet.
def update_game(game_id, winning_player, losing_players, winning_deck, losing_decks, date, notes):
    print(f"Updating game {game_id}...")

    date_object = datetime.strptime(date, "%Y-%m-%d").date()

    updated_game = Game.verbose_init(
        game_id = game_id,
        winning_player = winning_player,
        losing_players = losing_players,
        winning_deck = winning_deck,
        losing_decks = losing_decks,
        date = f"{date_object.day}/{date_object.month}/{date_object.year % 100}",
        notes = notes
    )

    games_worksheet = sheet.worksheet("Games")
    row_data = [
        updated_game.game_id,
        updated_game.winner.pilot,
        ", ".join([loser.pilot for loser in updated_game.losers]),
        updated_game.winner.deck_name,
        convert_deck_array_to_string([loser.deck_name for loser in updated_game.losers]),
        updated_game.date,
        updated_game.notes
    ]

    cell = games_worksheet.find(game_id)
    if cell is None:
        print(f"Game with ID {game_id} not found.")
        return

    row_number = cell.row
    games_worksheet.update(
        f"A{row_number}:{chr(64 + len(row_data))}{row_number}",
        [row_data],
        value_input_option="USER_ENTERED"
    )

    print(f"Game {game_id} updated successfully.")

# Deletes a game from the "Games" table in the "Games" worksheet.
def delete_game(game_id):
    print(f"Deleting game {game_id}...")

    games_worksheet = sheet.worksheet("Games")
    cell = games_worksheet.find(game_id)
    if cell is None:
        print(f"Game with ID {game_id} not found.")
        return

    row_number = cell.row
    games_worksheet.delete_rows(row_number)

    print(f"Game {game_id} deleted successfully.")

# Calculates the entire ELO history for all decks based on the recorded games.
def calculate_elos():
    print("Calculating ELOs...")
    for game in all_games:

        # Obtain Winning and Losing Decks
        winning_deck_object = get_deck_by_name(game.winner.deck_name)

        if winning_deck_object is None:
            print(f"Deck {game.winner.deck_name} not found in all_decks")
            return

        losing_decks = []
        for loser in game.losers:
            loser_deck_object = get_deck_by_name(loser.deck_name)

            if loser_deck_object is None:
                print(f"Deck {loser.deck_name} not found in all_decks")
                return

            losing_decks.append(loser_deck_object)

        # Calculate changes in ELO from this game
        winner_elo_change = 0

        for losing_deck_object in losing_decks:
            # Winner's elo changes for each losing deck
            winner_elo_change += winning_deck_object.k * (1 - winning_deck_object.odds_of_winning_against(losing_deck_object))
        
            # Loser's elo changes for the winning deck
            loser_elo_change = losing_deck_object.k * (0 - losing_deck_object.odds_of_winning_against(winning_deck_object))

            for other_losing_deck in losing_decks:
                if other_losing_deck == losing_deck_object:
                    continue
                # Loser's elo changes for each other losing deck
                loser_elo_change += losing_deck_object.k * (0.5 - losing_deck_object.odds_of_winning_against(other_losing_deck))
            
            # Log ELO change for the losing deck in the game record
            game.losers[losing_decks.index(losing_deck_object)].log_elo_change(losing_deck_object.get_current_elo(), loser_elo_change)
            
            # Update the losing deck's ELO
            losing_deck_object.add_elo(losing_deck_object.get_current_elo() + loser_elo_change, game.date, game.game_id)

        # Log ELO change for the winning deck in the game record
        game.winner.log_elo_change(winning_deck_object.get_current_elo(), winner_elo_change)

        #Update the winning deck's ELO
        winning_deck_object.add_elo(winning_deck_object.get_current_elo() + winner_elo_change, game.date, game.game_id)

calculate_elos()

def update_spreadsheet():
    print("Updating spreadsheet...")

    # Create a simple sheet of current Elos
    elo_worksheet = sheet.worksheet("ELOs")
    elo_worksheet.clear()

    sheet_data = []
    sheet_data.append(["Deck Name", "Elo", "Last Updated:", f"{date.today().strftime('%d/%m/%Y')}"])

    for deck in all_decks:
        sheet_data.append([deck.name, deck.get_current_elo()])

    elo_worksheet.append_rows(sheet_data)

    # Create a graphable sheet of Elo history
    history_worksheet = sheet.worksheet("ELO History")
    history_worksheet.clear()

    sheet_data = []
    sheet_data.append(["Date"] + [deck.name for deck in all_decks])
    deck_count = 0
    for deck in all_decks:
        for entry in deck.elo_history:
            if len(sheet_data) > 1 and entry["date"] == sheet_data[-1][0] and deck.name == sheet_data[0][deck_count + 1]:
                sheet_data[-1][-1] = entry["elo"]
                continue
            sheet_data.append([entry["date"]] + ([""] * deck_count) + [entry["elo"]])
        deck_count += 1

    history_worksheet.append_rows(sheet_data, value_input_option='USER_ENTERED')
    
    print("Spreadsheet updated successfully.")

# Asks for user input to select a deck by name, with support for partial matches and multiple results.
# Returns the selected deck object.
def user_select_deck(message="Please enter a deck name: "):
    user_input = input(message)

    found_decks = []
    while len(found_decks) == 0:
        pattern = re.compile(user_input, re.IGNORECASE)

        for deck in all_decks:
            if pattern.search(deck.name):
                found_decks.append(deck)

        if len(found_decks) == 0:
            user_input = input("No decks found with that name. Please try again: ")

    selected_deck = None
    if len(found_decks) == 1:
        selected_deck = found_decks[0]

    if len(found_decks) > 1:
        print("Multiple decks found with that name:")
        for i in range(len(found_decks)):
            print(f" - [{i}] {found_decks[i]['deck_name']}")
        choice = input("Please enter the number of the deck you would like to select: ")

    while selected_deck is None:
        try:
            choice = int(choice)
            if choice < 0 or choice >= len(found_decks):
                choice = input("Invalid choice. Please try again: ")
            else:
                selected_deck = found_decks[choice]
        except ValueError:
                choice = input("Invalid choice. Please try again: ")
    
    print(f"You have selected: {selected_deck.name}")
    return selected_deck
