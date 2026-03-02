import json

class Game:
    def __init__(self, game_id, winner, losers, date, notes):
        self.game_id = game_id
        self.winner = winner  # Deck_Performance object
        self.losers = losers  # List of Deck_Performance objects
        self.date = date
        self.notes = notes

    @classmethod
    def verbose_init(cls, game_id, winning_player, losing_players, winning_deck, losing_decks, date, notes):
        winner = Deck_Performance(winning_deck, winning_player)
        losers = [Deck_Performance(losing_decks[i], losing_players[i]) for i in range(len(losing_players))]
        return cls(game_id=game_id, winner=winner, losers=losers, date=date, notes=notes)

    @classmethod
    def from_sheet(cls, game_id, winning_player, losing_players, winning_deck, losing_decks, date, notes):
        return cls.verbose_init(game_id, winning_player, losing_players.split(", "), winning_deck, extract_decks_from_string(losing_decks), date, notes)

    @classmethod
    def from_json(cls, data):
        winner = Deck_Performance.from_json(data["winner"])
        losers = [Deck_Performance.from_json(deck) for deck in data["losers"]]
        return cls(game_id=data["game_id"], winner=winner, losers=losers, date=data["date"], notes=data["notes"])

    def __repr__(self):
        return f"Game(game_id={self.game_id}, winner={self.winner}, losers={self.losers}, date={self.date}, notes={self.notes})"
    
    def json(self):
        return {
            "game_id": self.game_id,
            "winner": self.winner.json(),
            "losers": [loser.json() for loser in self.losers],
            "date": self.date,
            "notes": self.notes
        }
    
class Deck_Performance:
    def __init__(self, deck_name, pilot):
        self.deck_name = deck_name
        self.pilot = pilot
        self.elo_before = None
        self.elo_after = None
    
    @classmethod
    def from_json(cls, data):
        obj = cls(deck_name=data["name"], pilot=data["pilot"])
        obj.elo_before = data.get("elo_before")
        obj.elo_after = data.get("elo_after")
        return obj

    def __repr__(self):
        return f"Deck_Performance(deck_name={self.deck_name}, pilot={self.pilot}, elo_before={self.elo_before}, elo_after={self.elo_after})"
    
    def json(self):
        return {"deck_name": self.deck_name, "pilot": self.pilot, "elo_before": self.elo_before, "elo_after": self.elo_after}
    
    def log_elo_change(self, elo_before, elo_change):
        self.elo_before = elo_before
        self.elo_after = elo_before + elo_change

# Creates an array of deck names from a string that may contain quoted names with commas.
def extract_decks_from_string(list_of_deck_names):
    decks = []
    current_deck = ""
    in_quotes = False
    i = 0
    
    while i < len(list_of_deck_names):
        char = list_of_deck_names[i]
        
        if char == '"':
            # Toggle quote state without adding the quote to the deck name
            in_quotes = not in_quotes
            i += 1
        elif char == ',' and not in_quotes:
            # Found a separator comma (not inside quotes)
            if current_deck.strip():
                decks.append(current_deck.strip())
            current_deck = ""
            i += 1
            # Skip the space after the comma if it exists
            if i < len(list_of_deck_names) and list_of_deck_names[i] == ' ':
                i += 1
        else:
            current_deck += char
            i += 1
    
    # Don't forget the last deck
    if current_deck.strip():
        decks.append(current_deck.strip())
    
    return decks