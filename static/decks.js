fetch("/get_all_decks")
    .then(response => response.json())
    .then(data => {
        const decksContainer = document.getElementById("decks_page_list");
        data.forEach(deck => {
            const deckElement = document.createElement("div");
            deckElement.classList.add("deck_item");
            deckElement.classList.add("bubble");
            deckElement.textContent = deck.name;

            deckElement.addEventListener("click", () => {
                fetch(`/get_stats?deck_name=${encodeURIComponent(deck.name)}`)
                    .then(response => response.json())
                    .then(data => {
                        const deckDetails = document.getElementById("deck_details");
                        deckDetails.style.display = "block";
                        if (window.innerWidth <= 800) document.getElementById("decks_page_list").style.display = "none"
                        deckDetails.innerHTML = `
                            <button id="back_to_list_button">Back</button>
                            <div class="flex-row">
                                <img id="deck_image" src="" alt="Deck Image">
                                <div>
                                    <h3>${data.deck_name}</h3>
                                    <p><strong>Owner:</strong> ${data.owner}</p>
                                    <p><strong>Bracket:</strong> ${data.bracket}</p>
                                    <p><strong>Tags:</strong> ${data.tags}</p>
                                    <p><strong>Games Played:</strong> ${data.games_played}</p>
                                    <p><strong>Last Played:</strong> ${data.last_played.date} (Game ID: ${data.last_played.game_id})</p>
                                    <p><strong>Win Rate:</strong> ${(data.win_rate * 100).toFixed(2)}% (${Math.floor(data.win_rate * data.games_played)} wins)</p>
                                    <p><strong>ELO:</strong> ${data.current_elo.toFixed(0)}</p>
                                    <p><strong>Average Opponent ELO:</strong> ${data.avrg_opponent_elo.toFixed(2)}</p>
                                    <p><strong>Average Opponent ELO When Win:</strong> ${data.avrg_opponent_elo_when_win.toFixed(2)}</p>
                                    <p><strong>Average Opponent ELO When Lose:</strong> ${data.avrg_opponent_elo_when_lose.toFixed(2)}</p>
                                </div>
                            </div>
                            <table id="deck_opponents"></table>
                        `;

                        document.getElementById("back_to_list_button").addEventListener("click", () => {
                            deckDetails.style.display = "none";
                            document.getElementById("decks_page_list").style.display = "block";
                        });
                        
                        const opponents_table = document.getElementById("deck_opponents");
                        opponents_table.innerHTML = "<tr><th>Opponent</th><th>G</th><th>W</th><th>L</th><th>W%</th></tr>"; // Clear previous content and add headers
                        for (let opponent of data.opponents) {
                            let row = document.createElement("tr");
                            let cell1 = document.createElement("td");
                            let cell2 = document.createElement("td");
                            let cell3 = document.createElement("td");
                            let cell4 = document.createElement("td");
                            let cell5 = document.createElement("td");
                            cell1.innerHTML = opponent.name;
                            cell2.innerHTML = opponent.games_played_vs;
                            cell3.innerHTML = opponent.wins_vs;
                            cell4.innerHTML = opponent.losses_vs;
                            cell5.innerHTML = (opponent.win_rate_vs * 100).toFixed(0) + "%";
                            row.appendChild(cell1);
                            row.appendChild(cell2);
                            row.appendChild(cell3);
                            row.appendChild(cell4);
                            row.appendChild(cell5);
                            opponents_table.appendChild(row);
                        }

                        fetch(`https://api.scryfall.com/cards/named?exact=${deck.name.split(" ").join("+")}`)
                            .then(response => response.json())
                            .then(data => {
                                console.log("Scryfall data:", data);
                                if (data.image_uris && data.image_uris.normal) {
                                    document.getElementById("deck_image").src = data.image_uris.normal;
                                    document.getElementById("deck_image").style.display = "block";
                                } else {
                                    document.getElementById("deck_image").style.display = "none";
                                }
                            })
                    });
            });

            decksContainer.appendChild(deckElement);
        });
    });

document.getElementById("deck_search_input").addEventListener("input", function() {
    const searchTerm = this.value.toLowerCase();
    const deckItems = document.querySelectorAll(".deck_item");
    deckItems.forEach(item => {
        if (item === this) return; // Skip the search input itself
        if (item.textContent.toLowerCase().includes(searchTerm)) {
            item.style.display = "block";
        } else {
            item.style.display = "none";
        }
    });
});