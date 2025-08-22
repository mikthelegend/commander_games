import gspread
from datetime import date
from google.oauth2.service_account import Credentials

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

def get_all_decks():
    print("Fetching all decks...")
    decks = []
    for row in sheet.worksheet("Stats").get_all_values()[1:]:
        deck = {
            "deck_name": row[0],
            "elos": [],          # List of elo, date pairs
            "k": 32,             # Starting K-factor
        }
        decks.append(deck)
    return decks

all_decks = get_all_decks()

def get_deck_by_name(deck_name):
    for deck in all_decks:
        if deck["deck_name"] == deck_name:
            return deck
    return None

def extract_decks_from_string(list_of_decks):
    final_array = []

    first_split = list_of_decks.split(", ")
    for item in first_split:
        if '"' not in item:
            final_array.append(item)

    quote_decks = list_of_decks.split('"')
    for i in range(1, len(quote_decks), 2):
        final_array.append(quote_decks[i])

    return final_array

def get_all_games():
    print("Fetching all games...")
    games = []
    for row in sheet.worksheet("Games").get_all_values()[1:]:
        game = {
            "game_id": row[0],
            "winning_player": row[1],
            "losing_players": extract_decks_from_string(row[2]),
            "winning_deck": row[3],
            "losing_decks": extract_decks_from_string(row[4]),
            "date": row[5],
        }
        games.append(game)
    return games

all_games = get_all_games()

def games_with(deck_name):
    games = []
    for game in all_games:
        if deck_name in game["losing_decks"] or deck_name == game["winning_deck"]:
            games.append(game)
    return games

def expected_outcome(your_elo, their_elo):
    return 1 / (1 + 10 ** (abs(their_elo - your_elo) / 400))

# Calculates the ELO of each deck based on the games played, updating their ELO ratings accordingly.
def calculate_elos():
    print("Calculating ELOs...")
    for game in all_games:
        # Obtain Winning and Losing Decks
        winning_deck = get_deck_by_name(game["winning_deck"])

        if winning_deck is None:
            print(f"Deck {game['winning_deck']} not found in all_decks")
            return
        
        if winning_deck["elos"] == []:
            winning_deck["elos"].append({"elo": 1000, "date": game["date"]})

        losing_decks = []
        for losing_deck_name in game["losing_decks"]:
            losing_deck = get_deck_by_name(losing_deck_name)

            if losing_deck is None:
                print(f"Deck {losing_deck_name} not found in all_decks")
                return
            
            if losing_deck["elos"] == []:
                losing_deck["elos"].append({"elo": 1000, "date": game["date"]})
            
            losing_decks.append(losing_deck)

        # Calculate changes in ELO from this game
        winner_elo_change = 0

        for losing_deck in losing_decks:
            # Winner's elo changes for each losing deck
            winner_elo_change += winning_deck["k"] * (1 - expected_outcome(winning_deck["elos"][-1]["elo"], losing_deck["elos"][-1]["elo"]))
        
            # Loser's elo changes for the winning deck
            loser_elo_change = losing_deck["k"] * (0 - expected_outcome(losing_deck["elos"][-1]["elo"], winning_deck["elos"][-1]["elo"]))

            for other_losing_deck in losing_decks:
                if other_losing_deck == losing_deck:
                    continue
                # Loser's elo changes for each other losing deck
                loser_elo_change += losing_deck["k"] * (0.5 - expected_outcome(losing_deck["elos"][-1]["elo"], other_losing_deck["elos"][-1]["elo"]))
            
            # Update ELOs
            new_loser_elo = {
                "elo": losing_deck["elos"][-1]["elo"] + loser_elo_change,
                "date": game["date"]
            }
            losing_deck["elos"].append(new_loser_elo)
            
        #Update the winning deck's ELO
        new_winner_elo = {
            "elo": winning_deck["elos"][-1]["elo"] + winner_elo_change,
            "date": game["date"]
        }
        winning_deck["elos"].append(new_winner_elo)

        # if (debug):
        #     print("" + "=" * 40)
        #     print(f"Game ID: {game['game_id']}")
        #     print(f"Updated {winning_deck['deck_name']} to ({winning_deck["elos"][-1]["elo"]}, {winning_deck["elos"][-1]["date"]})")
        #     for losing_deck in losing_decks:
        #         print(f"Updated {losing_deck['deck_name']} to ({losing_deck["elos"][-1]["elo"]}, {losing_deck["elos"][-1]["date"]})")

def update_spreadsheet():
    print("Updating spreadsheet...")

    elo_worksheet = sheet.worksheet("ELOs")
    elo_worksheet.clear()

    sheet_data = []
    sheet_data.append(["Deck Name", "Elo", "Last Updated:", f"{date.today().strftime('%d/%m/%Y')}"])

    for deck in all_decks:
        sheet_data.append([deck["deck_name"], deck["elos"][-1]["elo"] if deck["elos"] else 1000])

    elo_worksheet.append_rows(sheet_data)

    # Create a graphable sheet of Elo history
    history_worksheet = sheet.worksheet("ELO History")
    history_worksheet.clear()

    sheet_data = []
    sheet_data.append(["Date"] + [deck["deck_name"] for deck in all_decks])
    deck_count = 0
    for deck in all_decks:
        for elo in deck["elos"]:
            sheet_data.append([elo["date"]] + ([""] * deck_count) + [elo["elo"]])
        deck_count += 1

    history_worksheet.append_rows(sheet_data, value_input_option='USER_ENTERED')
    
    print("Spreadsheet updated successfully.")
