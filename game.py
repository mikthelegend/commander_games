import json

class Game:
    def __init__(self, game_id, winning_player, losing_players, winning_deck, losing_decks, date, notes):
        self.game_id = game_id
        self.winning_player = winning_player
        self.losing_players = losing_players
        self.winning_deck = winning_deck
        self.losing_decks = losing_decks
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
            "winning_deck": self.winning_deck,
            "losing_decks": self.losing_decks,
            "date": self.date,
            "notes": self.notes
        }
    
    def get_winning_player(self):
        return self.winning_player
    
    def get_losing_players(self):
        return self.losing_players
    
    def get_winning_deck(self):
        return self.winning_deck
    
    def get_losing_decks(self):
        return self.losing_decks
    
    def get_date(self):
        return self.date
    
    def get_notes(self):
        return self.notes
    