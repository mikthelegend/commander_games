import json
from game import Game
from deck import Deck

def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

def load_data():
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
            games = [Game(**game_data) for game_data in data.get("games", [])]
            decks = [Deck(**deck_data) for deck_data in data.get("decks", [])]
            return {"games": games, "decks": decks}
    except FileNotFoundError:
        return {}