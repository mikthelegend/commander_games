import gspread
from datetime import date
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
        deck = Deck(row[0])
        decks.append(deck)
    return decks

all_decks = get_all_decks()

def get_deck_by_name(deck_name):
    for deck in all_decks:
        if deck.name == deck_name:
            return deck
    return None

# Creates an array of deck names from a string that may contain quoted names with commas.
def extract_decks_from_string(list_of_deck_names):
    final_array = []

    first_split = list_of_deck_names.split(", ")
    for item in first_split:
        if '"' not in item:
            final_array.append(item)

    quote_decks = list_of_deck_names.split('"')
    for i in range(1, len(quote_decks), 2):
        final_array.append(quote_decks[i])

    return final_array

# Converts an array of deck names into a string, quoting names that contain commas.
def convert_deck_array_to_string(deck_array):
    final_string = ""
    for deck in deck_array:
        if ", " in deck:
            final_string += f'"{deck}", '
        else:
            final_string += f"{deck}, "
    return final_string[:-2]  # Remove trailing comma and space

# Fetches all games from the "Games" worksheet and returns them as a list of dictionaries.
def get_all_games():
    print("Fetching all games...")
    games = []
    for row in sheet.worksheet("Games").get_all_values()[1:]:
        game = Game(row[0], row[1], extract_decks_from_string(row[2]), row[3], extract_decks_from_string(row[4]), row[5], row[6])
        games.append(game)
    return games

all_games = get_all_games()

def get_all_players():
    players = set()
    for game in all_games:
        players.add(game.winning_player)
        for loser in game.losing_players:
            players.add(loser)
    return list(players)

all_players = get_all_players()

# Adds a new game to the all_games list and updates the "Games" table in the "Games" worksheet.
def add_new_game(winning_player, losing_players, winning_deck, losing_decks, date, notes):
    print("Adding new game...")
    new_game = Game(
        game_id = str(len(all_games) + 1),
        winning_player = winning_player,
        losing_players = losing_players,
        winning_deck = winning_deck,
        losing_decks = losing_decks,
        date = date,
        notes = notes
    )

    all_games.append(new_game)

    games_worksheet = sheet.worksheet("Games")
    games_worksheet.append_row([
        new_game.game_id,
        new_game.winning_player,
        ", ".join(new_game.losing_players),
        new_game.winning_deck,
        convert_deck_array_to_string(new_game.losing_decks),
        new_game.date,
        new_game.notes
    ])
    print("New game added successfully.")

    calculate_elos()
    update_spreadsheet()


# Calculates the entire ELO history for all decks based on the recorded games.
def calculate_elos():
    print("Calculating ELOs...")
    for game in all_games:

        # Obtain Winning and Losing Decks
        winning_deck = get_deck_by_name(game.winning_deck)

        if winning_deck is None:
            print(f"Deck {game.winning_deck} not found in all_decks")
            return

        if len(winning_deck.elo_history) == 0:
            winning_deck.add_elo(1000, game.date)

        losing_decks = []
        for losing_deck_name in game.losing_decks:
            losing_deck = get_deck_by_name(losing_deck_name)

            if losing_deck is None:
                print(f"Deck {losing_deck_name} not found in all_decks")
                return
            
            if len(losing_deck.elo_history) == 0:
                losing_deck.add_elo(1000, game.date)

            losing_decks.append(losing_deck)

        # Calculate changes in ELO from this game
        winner_elo_change = 0

        for losing_deck in losing_decks:
            # Winner's elo changes for each losing deck
            winner_elo_change += winning_deck.k * (1 - winning_deck.odds_of_winning_against(losing_deck))
        
            # Loser's elo changes for the winning deck
            loser_elo_change = losing_deck.k * (0 - losing_deck.odds_of_winning_against(winning_deck))

            for other_losing_deck in losing_decks:
                if other_losing_deck == losing_deck:
                    continue
                # Loser's elo changes for each other losing deck
                loser_elo_change += losing_deck.k * (0.5 - losing_deck.odds_of_winning_against(other_losing_deck))
            
            # Update the losing deck's ELO
            losing_deck.add_elo(losing_deck.get_current_elo() + loser_elo_change, game.date)
            
        #Update the winning deck's ELO
        winning_deck.add_elo(winning_deck.get_current_elo() + winner_elo_change, game.date)

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
