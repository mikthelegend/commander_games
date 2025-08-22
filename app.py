from flask import Flask
import main

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/health")
def health_check():
    return "OK", 200

@app.route("/update")
def perform_elo_update():
    main.all_decks = main.get_all_decks()
    main.all_games = main.get_all_games()
    main.calculate_elos()
    main.update_spreadsheet()
    return "ELOs updated successfully", 200
