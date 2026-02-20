function generateGameCard(game) {
    const split = game.date.split("/");
    const date = new Date('20' + split[2], split[1]-1, split[0])
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
                    <b><i>#</i></b>${game.game_id}
                </div>
            </div>
            <div class="card_body">
                <div>
                    <div>
                        <i class="fa fa-arrow-up"></i><b>Winner:</b> &nbsp; ${game.winning_player}
                    </div>
                    <div class="deck_with_elo">
                        ${game.winning_deck.name}
                        <span class="elo_change">
                            <i class="fa-solid fa-angles-up"></i>${(game.winning_deck.elo_after - game.winning_deck.elo_before < 0 ? "" : "+") + Math.round(game.winning_deck.elo_after - game.winning_deck.elo_before)}
                        </span>
                    </div>
                </div>
                <div>
                    <div>
                        <i class="fa fa-arrow-down"></i><b>Losers:</b> &nbsp; ${game.losing_players.join(", ")}
                    </div>
                    ${game.losing_decks.map(deck => `
                        <div class="deck_with_elo">
                            <span>${deck.name}</span>
                            <span class="elo_change">
                                ${(deck.elo_after - deck.elo_before < 0 ? "" : "+") + Math.round(deck.elo_after - deck.elo_before)}
                            </span>
                        </div>
                    `).join("")}
                </div>
            </div>
            <div class="card_footer"> 
                ${game.notes}
            </div>
        `;
}