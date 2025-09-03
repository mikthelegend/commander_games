from flask import Flask
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import main
from plot import get_elo_history_data

flask_app = Flask(__name__)
dash_app = Dash(__name__, server=flask_app, url_base_pathname='/plot/')

@flask_app.route("/")
def hello_world():
    return "Hello, World!"

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

@flask_app.route("/plot_elos")
def redirect_to_plot():
    return flask_app.redirect("/plot/")

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
