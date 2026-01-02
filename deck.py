import json

class Deck:
    def __init__(self, name, k=32):
        self.name = name
        self.k = k
        self.elo_history = []  # List of dictionaries with 'elo' and 'date' keys

    def __repr__(self):
        return f"Deck(name={self.name}, k={self.k}, elo_history={self.elo_history})"
    
    def json(self):
        return {"name": self.name, "k": self.k, "elo_history": self.elo_history}
    
    def add_elo(self, elo, date):
        self.elo_history.append({"elo": elo, "date": date})

    def get_current_elo(self):
        if self.elo_history:
            return self.elo_history[-1]["elo"]
        return 1000
    
    # New method to calculate odds of winning against another deck
    def odds_of_winning_against(self, opponent):
        expected = 1 / (1 + 10 ** ((opponent.get_current_elo() - self.get_current_elo()) / 400))
        return expected