import json

class Game:
    def __init__(self, game_id, winning_player, losing_players, winning_deck, losing_decks, date, notes):
        self.game_id = game_id
        self.winning_player = winning_player
        self.losing_players = losing_players
        self.winning_deck = Deck_Performance(winning_deck)
        self.losing_decks = [Deck_Performance(deck) for deck in losing_decks]
        self.date = date
        self.notes = notes

    def __repr__(self):
        return (f"Game(game_id={self.game_id}, winning_player={self.winning_player}, "
                f"losing_players={self.losing_players}, winning_deck={self.winning_deck}, "
                f"losing_decks={self.losing_decks}, date={self.date}, notes={self.notes})")
    
    def json(self):
        return {
            "game_id": self.game_id,
            "winning_player": self.winning_player,
            "losing_players": self.losing_players,
            "winning_deck": self.winning_deck.json(),
            "losing_decks": [deck.json() for deck in self.losing_decks],
            "date": self.date,
            "notes": self.notes
        }
    
class Deck_Performance:
    def __init__(self, deck_name):
        self.name = deck_name
        self.elo_before = None
        self.elo_after = None

    def __repr__(self):
        return f"Deck_Performance(deck_name={self.name}, elo_before={self.elo_before}, elo_after={self.elo_after})"
    
    def json(self):
        return {"name": self.name, "elo_before": self.elo_before, "elo_after": self.elo_after}
    
    def log_elo_change(self, elo_before, elo_change):
        self.elo_before = elo_before
        self.elo_after = elo_before + elo_change