function generateGameCard(game) {
    return `<strong>Game ID:</strong> ${game.game_id} <strong>Date:</strong> ${game.date} <br>
            <strong>Winner:</strong> ${game.winning_player} <br>(${game.winning_deck.name} [${(game.winning_deck.elo_after - game.winning_deck.elo_before < 0 ? "" : "+") + Math.round(game.winning_deck.elo_after - game.winning_deck.elo_before)}]) <br>
            <strong>Losers:</strong> ${game.losing_players.join(", ")} <br>
            <strong>Losing Decks:</strong> <br>${game.losing_decks.map(deck => `${deck.name} [${(deck.elo_after - deck.elo_before < 0 ? "" : "+") + Math.round(deck.elo_after - deck.elo_before)}]`).join("<br>")} <br>
            <strong>Notes:</strong> <br>${game.notes}`;
}