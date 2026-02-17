function generateGameCard(game) {
    const split = game.date.split("/");
    const date = new Date('20' + split[2], split[1], split[0])
    const options = {
        weekday: "short",
        day: "numeric",
        month: "short",
        year: "numeric",
    }
    return `
            <div class="card_header">
                <div>
                    ${date.toLocaleDateString("en-AU", options)}
                </div>
                <div>
                    <b>ID</b> ${game.game_id}
                </div>
            </div>
            <div class="card_body">
                <div>
                    <div><b>Winner:</b> ${game.winning_player}</div>
                    <div>${game.winning_deck.name} [${(game.winning_deck.elo_after - game.winning_deck.elo_before < 0 ? "" : "+") + Math.round(game.winning_deck.elo_after - game.winning_deck.elo_before)}]</div>
                </div>
                <br>
                <div>
                    <div><b>Losers:</b> ${game.losing_players.join(", ")}</div>
                    ${game.losing_decks.map(deck => `${deck.name} [${(deck.elo_after - deck.elo_before < 0 ? "" : "+") + Math.round(deck.elo_after - deck.elo_before)}]`).join("<br>")} <br>
                </div>
            </div>
            <div class="card_footer"> 
                <!--<b>Notes:</b> <br>-->
                ${game.notes}
            </div>
        `;
}