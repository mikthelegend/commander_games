function generateGameCard(game) {
    return `
        <b>Date:</b> ${game.date} &emsp;&emsp;&emsp;&emsp;&ensp; <b>Game ID:</b> ${game.game_id} <br>
        <br>
        <b>Winner:</b> ${game.winning_player} <br>
        ${game.winning_deck.name} [${(game.winning_deck.elo_after - game.winning_deck.elo_before < 0 ? "" : "+") + Math.round(game.winning_deck.elo_after - game.winning_deck.elo_before)}] <br>
        <br>
        <b>Losers:</b> ${game.losing_players.join(", ")} <br>
        ${game.losing_decks.map(deck => `${deck.name} [${(deck.elo_after - deck.elo_before < 0 ? "" : "+") + Math.round(deck.elo_after - deck.elo_before)}]`).join("<br>")} <br>
        <br>
        <b>Notes:</b> <br>
        ${game.notes}
        `;
}