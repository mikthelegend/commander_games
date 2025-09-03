from flask import Flask
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import main
import plot

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

# ------------[ Dash app ]------------

app = Dash(__name__)

app.layout = html.Div([
    html.H4('Deck ELO Over Time'),
    dcc.Graph(id="graph"),
])

@app.callback(
    Output("graph", "figure"),
    Input("graph", "id")  # Dummy input to trigger the callback once
)
def update_line_chart():
    df = plot.get_elo_history_Data()
    fig = px.line(df, x="Date", y="Elo", color="Deck", title='Deck ELO Over Time', markers=True, line_shape='hv')
    return fig
