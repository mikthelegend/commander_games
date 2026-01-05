import main
import util

main.update_spreadsheet()

data = {
    "decks": [deck.json() for deck in main.all_decks],
    "games": [game.json() for game in main.all_games]
}

util.save_data(data)
