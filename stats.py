import main

# Analyzes a deck's performance and returns various statistics about it
# 
# Things to see:
# - The win rate of the deck
# - The current ELO
# - The average ELO of opponents
# - The average ELO of opponents when the deck wins
# - The average ELO of opponents when the deck loses
# - The decks most commonly played against
# - The decks winrate against each opponent
# - The decks lose rate against each opponent

def analyze_deck(deck_name):

    deck_object = main.get_deck_by_name(deck_name)
    if deck_object is None:
        print(f"Deck {deck_name} not found in all_decks")
        return

    games_played = 0
    wins = 0

    # Sums the ELO of all opponents across all games to calculate the average ELO of opponents faced
    avrg_opponent_elo = 0
    num_opponents = 0

    # Sums the ELO of opponents when the deck wins to calculate the average ELO of opponents faced in wins
    avrg_opponent_elo_when_win = 0
    num_opponents_when_win = 0

    # Sums the ELO of opponents when the deck loses to calculate the average ELO of opponents faced in losses
    avrg_opponent_elo_when_lose = 0
    num_opponents_when_lose = 0

    # Libraries to count the number of times the deck has faced each opponent and the number of wins against each opponent
    opponent_decks = {}
    opponent_decks_when_win = {}

    for game in main.all_games:
        if game.winning_deck.name == deck_name:
            games_played += 1
            wins += 1 

            opponent_elos = [deck.elo_before for deck in game.losing_decks]
            avrg_opponent_elo += sum(opponent_elos)
            avrg_opponent_elo_when_win += sum(opponent_elos)
            num_opponents += len(game.losing_decks)
            num_opponents_when_win += len(game.losing_decks)

            for deck in game.losing_decks:
                if deck.name not in opponent_decks:
                    opponent_decks[deck.name] = 0
                opponent_decks[deck.name] += 1

                if deck.name not in opponent_decks_when_win:
                    opponent_decks_when_win[deck.name] = 0
                opponent_decks_when_win[deck.name] += 1

        elif deck_name in [deck.name for deck in game.losing_decks]:
            games_played += 1

            opponents_elos = [game.winning_deck.elo_before] + [deck.elo_before for deck in game.losing_decks if deck.name != deck_name]
            avrg_opponent_elo += sum(opponents_elos)
            avrg_opponent_elo_when_lose += sum(opponents_elos)
            num_opponents += len(game.losing_decks)
            num_opponents_when_lose += len(game.losing_decks)

            for deck in game.losing_decks + [game.winning_deck]:
                if deck.name == deck_name:
                    continue
                if deck.name not in opponent_decks:
                    opponent_decks[deck.name] = 0
                opponent_decks[deck.name] += 1

    stats = {
        "deck_name": deck_name,
        "games_played": games_played,
        "last_played": {"date": deck_object.get_current_elo_entry()["date"], "game_id": deck_object.get_current_elo_entry()["game_id"]},
        "win_rate": wins / games_played if games_played > 0 else 0,
        "current_elo": deck_object.get_current_elo(),
        "avrg_opponent_elo": avrg_opponent_elo / num_opponents if num_opponents > 0 else 0,
        "avrg_opponent_elo_when_win": avrg_opponent_elo_when_win / num_opponents_when_win if num_opponents_when_win > 0 else 0,
        "avrg_opponent_elo_when_lose": avrg_opponent_elo_when_lose / num_opponents_when_lose if num_opponents_when_lose > 0 else 0,
        "opponents": []
    }

    for opponent in opponent_decks:
        if opponent not in opponent_decks_when_win:
            opponent_decks_when_win[opponent] = 0

        stats["opponents"].append({
            "name": opponent,
            "games_played_vs": opponent_decks[opponent],
            "wins_vs": opponent_decks_when_win[opponent],
            "losses_vs": opponent_decks[opponent] - (opponent_decks_when_win[opponent]),
            "win_rate_vs": (opponent_decks_when_win[opponent] / opponent_decks[opponent]) if opponent_decks[opponent] > 0 else 0
        })

    stats["opponents"].sort(key=lambda x: (x["games_played_vs"], x["win_rate_vs"]), reverse=True)

    return stats

# Finds the highest recorded elo, lowest recorded elo, both currently and historically
def find_records():
    highest_current_elo = float('-inf')
    highest_elo_deck = None
    highest_elo_entry = None

    lowest_current_elo = float('inf')
    lowest_elo_deck = None
    lowest_elo_entry = None

    highest_elo_ever = float('-inf')
    highest_elo_ever_deck = None
    highest_elo_ever_entry = None

    lowest_elo_ever = float('inf')
    lowest_elo_ever_deck = None
    lowest_elo_ever_entry = None

    for deck in main.all_decks:
        current_elo = deck.get_current_elo()
        if current_elo > highest_current_elo:
            highest_current_elo = current_elo
            highest_elo_deck = deck.name
            highest_elo_entry = deck.get_current_elo_entry()
        if current_elo < lowest_current_elo:
            lowest_current_elo = current_elo
            lowest_elo_deck = deck.name
            lowest_elo_entry = deck.get_current_elo_entry()
        
        for entry in deck.elo_history:
            if entry["elo"] > highest_elo_ever:
                highest_elo_ever = entry["elo"]
                highest_elo_ever_deck = deck.name
                highest_elo_ever_entry = entry
            if entry["elo"] < lowest_elo_ever:
                lowest_elo_ever = entry["elo"]
                lowest_elo_ever_deck = deck.name
                lowest_elo_ever_entry = entry
    return {
        "highest_current": {
            "deck": highest_elo_deck,
            "elo_entry": highest_elo_entry
        },
        "lowest_current": {
            "deck": lowest_elo_deck,
            "elo_entry": lowest_elo_entry
        },
        "highest_ever": {
            "deck": highest_elo_ever_deck,
            "elo_entry": highest_elo_ever_entry
        },
        "lowest_ever": {
            "deck": lowest_elo_ever_deck,
            "elo_entry": lowest_elo_ever_entry
        }
    }