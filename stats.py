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

    avrg_opponent_elo = 0
    num_opponents = 0

    avrg_opponent_elo_when_win = 0
    num_opponents_when_win = 0

    avrg_opponent_elo_when_lose = 0
    num_opponents_when_lose = 0

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

    stats = Deck_Stats(deck_name)

    stats.games_played = games_played
    stats.win_rate = wins / games_played if games_played > 0 else 0
    stats.current_elo = deck_object.get_current_elo()

    stats.avrg_opponent_elo = avrg_opponent_elo / num_opponents if num_opponents > 0 else 0
    stats.avrg_opponent_elo_when_win = avrg_opponent_elo_when_win / num_opponents_when_win if num_opponents_when_win > 0 else 0
    stats.avrg_opponent_elo_when_lose = avrg_opponent_elo_when_lose / num_opponents_when_lose if num_opponents_when_lose > 0 else 0

    stats.opponents = []
    for opponent in opponent_decks:
        if opponent not in opponent_decks_when_win:
            opponent_decks_when_win[opponent] = 0

        stats.opponents.append({
            "name": opponent,
            "games_played_vs": opponent_decks[opponent],
            "wins_vs": opponent_decks_when_win[opponent],
            "losses_vs": opponent_decks[opponent] - (opponent_decks_when_win[opponent] if opponent in opponent_decks_when_win else 0),
            "win_rate_vs": (opponent_decks_when_win[opponent] / opponent_decks[opponent]) if opponent in opponent_decks and opponent_decks[opponent] > 0 else 0
        })

    stats.opponents.sort(key=lambda x: (x["games_played_vs"], x["win_rate_vs"]), reverse=True)

    return stats


class Deck_Stats:
    def __init__(self, deck_name):
        self.deck_name = deck_name
        self.games_played = 0
        self.win_rate = 0
        self.current_elo = 0
        self.avrg_opponent_elo = 0
        self.avrg_opponent_elo_when_win = 0
        self.avrg_opponent_elo_when_lose = 0
        self.opponents = []

    def __repr__(self):
        return (f"Deck_Stats(deck_name={self.deck_name}, win_rate={self.win_rate}, current_elo={self.current_elo}, "
                f"avrg_opponent_elo={self.avrg_opponent_elo}, avrg_opponent_elo_when_win={self.avrg_opponent_elo_when_win}, "
                f"avrg_opponent_elo_when_lose={self.avrg_opponent_elo_when_lose}, opponents={self.opponents}, ")
    
    def json(self):
        return {
            "deck_name": self.deck_name,
            "games_played": self.games_played,
            "win_rate": self.win_rate,
            "current_elo": self.current_elo,
            "avrg_opponent_elo": self.avrg_opponent_elo,
            "avrg_opponent_elo_when_win": self.avrg_opponent_elo_when_win,
            "avrg_opponent_elo_when_lose": self.avrg_opponent_elo_when_lose,
            "opponents": self.opponents
        }

    def pretty_print(self):
        print(f"Deck Name: {self.deck_name}")
        print(f"Win Rate: {self.win_rate:.2%}")
        print(f"Current ELO: {self.current_elo}")
        print(f"Average Opponent ELO: {self.avrg_opponent_elo:.2f}")
        print(f"Average Opponent ELO When Win: {self.avrg_opponent_elo_when_win:.2f}")
        print(f"Average Opponent ELO When Lose: {self.avrg_opponent_elo_when_lose:.2f}")
        print("Opponents:")
        for opponent in self.opponents:
            print(f"  {opponent.name} - Games Played: {opponent['games_played_vs']}, Wins: {opponent['wins_vs']}, Losses: {opponent['losses_vs']}, Win Rate: {opponent['win_rate_vs']:.2%}")


# Finds the highest recorded elo, lowest recorded elo, both currently and historically
def find_records():
    highest_current_elo = float('-inf')
    highest_elo_deck = None

    lowest_current_elo = float('inf')
    lowest_elo_deck = None

    highest_elo_ever = float('-inf')
    highest_elo_ever_deck = None

    lowest_elo_ever = float('inf')
    lowest_elo_ever_deck = None

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
            if elo > highest_elo_ever:
                highest_elo_ever = elo
                highest_elo_ever_deck = deck.name
            if elo < lowest_elo_ever:
                lowest_elo_ever = elo
                lowest_elo_ever_deck = deck.name

    return {
        "highest_current": {
            "deck": highest_elo_deck,
            "elo": highest_current_elo
        },
        "lowest_current": {
            "deck": lowest_elo_deck,
            "elo": lowest_current_elo
        },
        "highest_ever": {
            "deck": highest_elo_ever_deck,
            "elo": highest_elo_ever
        },
        "lowest_ever": {
            "deck": lowest_elo_ever_deck,
            "elo": lowest_elo_ever
        }
    }