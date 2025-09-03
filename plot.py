from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import main

def get_elo_history_data():
    data = {"Date": [], "Elo": [], "Deck": []}
    for deck in main.all_decks:
        # Remove duplicate dates for the same deck, taking only the latest Elo for that date
        for entry in deck.elo_history:
            if len(data["Date"]) > 0 and entry["date"] == data["Date"][-1] and deck.name == data["Deck"][-1]:
                data["Elo"][-1] = entry["elo"]
                continue

            data["Date"].append(entry["date"])
            data["Elo"].append(entry["elo"])
            data["Deck"].append(deck.name)
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y')
    df.sort_values(by=["Date"], inplace=True)
    return df

if __name__ == "__main__":
    # Manual Plot
    df = get_elo_history_data()
    fig = px.line(df, x="Date", y="Elo", color="Deck", title='Deck ELO Over Time', markers=True, line_shape='hv')
    fig.show()