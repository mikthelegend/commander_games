function generateGameCard(game) {
    const card = document.createElement("div");
    card.className = "card";

    const split = game.date.split("/");
    const date = new Date('20' + split[2], split[1]-1, split[0])
    const options = {
        weekday: "short",
        day: "numeric",
        month: "short",
        year: "numeric",
    }
    card.innerHTML = `
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
                        <i class="fa fa-arrow-up"></i><b>Winner:</b> &nbsp;
                    </div>
                    <div class="deck_with_elo">
                        <span>${game.winner.pilot}</span> - &nbsp;
                        <span>${game.winner.deck_name}</span>
                        <span class="elo_change">
                            <i class="fa-solid fa-angles-up"></i>${(game.winner.elo_after - game.winner.elo_before < 0 ? "" : "+") + Math.round(game.winner.elo_after - game.winner.elo_before)}
                        </span>
                    </div>
                </div>
                <div>
                    <div>
                        <i class="fa fa-arrow-down"></i><b>Losers:</b> &nbsp;
                    </div>
                    ${game.losers.map(loser => `
                        <div class="deck_with_elo">
                            <span>${loser.pilot}</span> - &nbsp;
                            <span>${loser.deck_name}</span>
                            <span class="elo_change">
                                ${(loser.elo_after - loser.elo_before < 0 ? "" : "+") + Math.round(loser.elo_after - loser.elo_before)}
                            </span>
                        </div>
                    `).join("")}
                </div>
            </div>
            <div class="card_footer"> 
                ${game.notes}
            </div>
        `;

    card.addEventListener("click", () => {
        window.location.href = `/games/${game.game_id}`;
    });

    return card;
}