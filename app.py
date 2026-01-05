from flask import Flask, render_template, request, send_from_directory
from dash import Dash, dcc, html
import plotly.express as px
import main
from plot import get_elo_history_data
import stats
import os

flask_app = Flask(__name__)
dash_app = Dash(__name__, server=flask_app, url_base_pathname='/plot/')

@flask_app.route("/")
def index():
    return render_template('index.html')

@flask_app.route("/stats")
def stats():
    main.all_decks = main.get_all_decks()
    main.all_games = main.get_all_games()
    main.calculate_elos()
    return render_template('stats.html')

@flask_app.route("/games")
def games():
    return render_template('games.html')

@flask_app.route("/log")
def log():
    return render_template('log.html')

@flask_app.route("/health")
def health_check():
    return "OK", 200

@flask_app.route("/update")
def perform_elo_update():
    main.all_decks = main.get_all_decks()
    main.all_games = main.get_all_games()
    main.calculate_elos()
    main.update_spreadsheet()
    return "ELOs updated successfully", 200

@flask_app.route("/matchup", methods=['GET'])
def matchup():
    deck_name = request.args.get('deck_name')
    deck = main.get_deck_by_name(deck_name)
    matchups = stats.generate_matchup(deck)
    return matchups

@flask_app.route("/records")
def get_records():
    return stats.find_records()

@flask_app.route("/get_all_decks")
def get_all_decks():
    return [deck.json() for deck in main.all_decks]

@flask_app.route("/get_all_games")
def get_all_games():
    return [game.json() for game in main.all_games]

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
