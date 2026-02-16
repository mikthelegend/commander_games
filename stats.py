import main

# Finds the closest rated decks and their elo differences
def generate_matchup(selected_deck):
    matchups = []
    for deck in main.all_decks:
        if deck != selected_deck:
            elo_diff =  deck.get_current_elo() - selected_deck.get_current_elo()
            matchups.append((deck.name, elo_diff))

    matchups.sort(key=lambda x: abs(x[1]))
    return matchups

# Finds the highest recorded elo, lowest recorded ele, both currently and historically
def find_records():
    highest_current_elo = float('-inf')
    highest_elo_deck = None

    lowest_current_elo = float('inf')
    lowest_elo_deck = None

    highest_historical_elo = float('-inf')
    highest_historical_elo_deck = None

    lowest_historical_elo = float('inf')
    lowest_historical_elo_deck = None

    for deck in main.all_decks:
        current_elo = deck.get_current_elo()
        if current_elo > highest_current_elo:
            highest_current_elo = current_elo
            highest_elo_deck = deck.name
        if current_elo < lowest_current_elo:
            lowest_current_elo = current_elo
            lowest_elo_deck = deck.name
        
        for entry in deck.elo_history:
            elo = entry["elo"]
            if elo > highest_historical_elo:
                highest_historical_elo = elo
                highest_historical_elo_deck = deck.name
            if elo < lowest_historical_elo:
                lowest_historical_elo = elo
                lowest_historical_elo_deck = deck.name

    return {
        "highest_current": {
            "deck": highest_elo_deck,
            "elo": highest_current_elo
        },
        "lowest_current": {
            "deck": lowest_elo_deck,
            "elo": lowest_current_elo
        },
        "highest_historical": {
            "deck": highest_historical_elo_deck,
            "elo": highest_historical_elo
        },
        "lowest_historical": {
            "deck": lowest_historical_elo_deck,
            "elo": lowest_historical_elo
        }
    }