from flask import Flask, render_template, request, send_from_directory
from dash import Dash, dcc, html
import plotly.express as px
import main
import util
from stats import analyze_deck, find_records
import json
from plot import get_elo_history_data
import os

flask_app = Flask(__name__)
dash_app = Dash(__name__, server=flask_app, url_base_pathname='/plot/')

# -------- Web Routes --------

@flask_app.route("/")
def index():
    return render_template('index.html')

@flask_app.route("/games")
def games():
    return render_template('games.html')

@flask_app.route("/stats")
def stats():
    return render_template('stats.html')

# -------- API Routes --------

@flask_app.route("/health")
def health_check():
    return "OK", 200

@flask_app.route("/update")
def perform_elo_update():
    main.all_decks = main.get_all_decks()
    main.all_games = main.get_all_games()
    main.calculate_elos()
    main.update_spreadsheet()
    util.save_data()
    return "ELOs updated successfully", 200

@flask_app.route("/new_game", methods=['POST'])
def new_game():
    data = json.loads(request.data)
    print(f"Received new game data: {data}")
    main.add_new_game(**data)
    perform_elo_update()  # Recalculate ELOs after adding the new game
    return request.data, 200

@flask_app.route("/get_stats", methods=['GET'])
def get_stats():
    deck_name = request.args.get('deck_name')
    results = analyze_deck(deck_name)
    return results, 200

@flask_app.route("/records")
def get_records():
    return find_records()

@flask_app.route("/get_all_decks")
def get_all_decks():
    return [deck.json() for deck in main.all_decks]

@flask_app.route("/get_all_games")
def get_all_games():
    return [game.json() for game in main.all_games]

@flask_app.route("/get_all_players")
def get_all_players():
    return main.all_players

@flask_app.route("/plot_elos")
def redirect_to_plot():
    return flask_app.redirect("/plot/")

@flask_app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(flask_app.root_path, 'static'), 'favicon.ico')

# ------------[ Dash app ]------------

dash_app.layout = html.Div([
    dcc.Graph(
        id="graph", 
        figure=px.line(
            get_elo_history_data(), 
            x="Date", 
            y="Elo", 
            color="Deck", 
            title='Deck ELO Over Time', 
            markers=True, 
            line_shape='hv'
        ),
        style={"height": "80vh"}
    ),
])
