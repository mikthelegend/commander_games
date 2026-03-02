import json

default_k = 32

class Deck:
    def __init__(self, name, bracket, owner, commander_id, tags, k=default_k, elo_history=None):
        self.name = name
        self.bracket = bracket
        self.owner = owner
        self.commander_id = commander_id
        self.tags = tags
        self.k = k
        if elo_history is None:
            self.elo_history = []
        else:
            self.elo_history = elo_history  # List of dictionaries with 'elo', 'date' & 'game_id' keys

    @classmethod
    def from_json(cls, data):
        return cls(
            name=data["name"],
            bracket=data["bracket"],
            owner=data["owner"],
            commander_id=data["commander_id"],
            tags=data["tags"],
            k=data.get("k", default_k),
            elo_history=data.get("elo_history", [])
        )

    def __repr__(self):
        return f"Deck(name={self.name}, bracket={self.bracket}, owner={self.owner}, commander_id={self.commander_id}, tags={self.tags}, k={self.k}, elo_history={self.elo_history})"
    
    def json(self):
        return {"name": self.name, "bracket": self.bracket, "owner": self.owner, "commander_id": self.commander_id, "tags": self.tags, "k": self.k, "elo_history": self.elo_history}

    def add_elo(self, elo, date, game_id):
        self.elo_history.append({"elo": elo, "date": date, "game_id": game_id})

    def get_current_elo(self):
        if self.elo_history:
            return self.elo_history[-1]["elo"]
        return 1000
    
    def get_current_elo_entry(self):
        if self.elo_history:
            return self.elo_history[-1]
        return {"elo": 1000, "date": None, "game_id": None}
    
    # New method to calculate odds of winning against another deck
    def odds_of_winning_against(self, opponent):
        expected = 1 / (1 + 10 ** ((opponent.get_current_elo() - self.get_current_elo()) / 400))
        return expected