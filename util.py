import json
import main
from game import Game
from deck import Deck

def save_data():
    with open('data.json', 'w') as f:
        data = {
            "decks": [deck.json() for deck in main.all_decks],
            "games": [game.json() for game in main.all_games]
        }
        json.dump(data, f, indent=4)
        print("Data saved to data.json")

def load_data():
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
            games = [Game(**game_data) for game_data in data.get("games", [])]
            decks = [Deck(**deck_data) for deck_data in data.get("decks", [])]
            return {"games": games, "decks": decks}
    except FileNotFoundError:
        return {}