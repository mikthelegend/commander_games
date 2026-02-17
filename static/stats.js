// Populate dropdown with deck names
let innerHTML = "";
fetch('/get_all_decks')
    .then(response => response.json())
    .then(data => {
        data.forEach(deck => {
            innerHTML += `<option value="${deck.name}">${deck.name}</option>`;
        });
        document.getElementById("deck_analysis_dropdown").innerHTML = innerHTML;
    });

document.getElementById("analyse_button").onclick = function() {
    let selected_deck = document.getElementById("deck_analysis_dropdown").value;
    console.log("Selected deck:", selected_deck);
    fetch(`/get_stats?deck_name=${encodeURIComponent(selected_deck)}`)
        .then(response => response.json())
        .then(data => {
            console.log("Deck analysis data:", data);

            document.getElementById("analysis_results_container").style.display = "block";

            document.getElementById("deck_name").innerHTML = data.deck_name;
            document.getElementById("deck_games_played").innerHTML = data.games_played;
            document.getElementById("deck_last_played").innerHTML = `${data.last_played.date} (Game ID: ${data.last_played.game_id})`;
            document.getElementById("deck_win_rate").innerHTML = (data.win_rate * 100).toFixed(2) + "%" + " (" + data.win_rate * data.games_played + " wins)";
            document.getElementById("deck_elo").innerHTML = data.current_elo.toFixed(0);
            document.getElementById("deck_avrg_opponent_elo").innerHTML = data.avrg_opponent_elo.toFixed(2);
            document.getElementById("deck_avrg_opponent_elo_when_win").innerHTML = data.avrg_opponent_elo_when_win.toFixed(2);
            document.getElementById("deck_avrg_opponent_elo_when_lose").innerHTML = data.avrg_opponent_elo_when_lose.toFixed(2);

            // Populate Mobile Data
            document.getElementById("deck_name_mobile").innerHTML = data.deck_name;
            document.getElementById("deck_games_played_mobile").innerHTML = data.games_played;
            document.getElementById("deck_last_played_mobile").innerHTML = `${data.last_played.date} (Game ID: ${data.last_played.game_id})`;
            document.getElementById("deck_win_rate_mobile").innerHTML = (data.win_rate * 100).toFixed(2) + "%" + " (" + data.win_rate * data.games_played + " wins)";
            document.getElementById("deck_elo_mobile").innerHTML = data.current_elo.toFixed(0);
            document.getElementById("deck_avrg_opponent_elo_mobile").innerHTML = data.avrg_opponent_elo.toFixed(2);
            document.getElementById("deck_avrg_opponent_elo_when_win_mobile").innerHTML = data.avrg_opponent_elo_when_win.toFixed(2);
            document.getElementById("deck_avrg_opponent_elo_when_lose_mobile").innerHTML = data.avrg_opponent_elo_when_lose.toFixed(2);
            
            // Populate opponents tables
            const opponents_table = document.getElementById("deck_opponents");
            const opponents_table_mobile = document.getElementById("deck_opponents_mobile");
            opponents_table.innerHTML = "<tr><th>Opponent</th><th>Games</th><th>Wins</th><th>Losses</th><th>Win Rate</th></tr>"; // Clear previous content and add headers
            opponents_table_mobile.innerHTML = "<tr><th>Opponent</th><th>G</th><th>W</th><th>L</th><th>%W</th></tr>"; // Clear previous content and add headers
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
                cell5.innerHTML = (opponent.win_rate_vs * 100).toFixed(2) + "%";
                row.appendChild(cell1);
                row.appendChild(cell2);
                row.appendChild(cell3);
                row.appendChild(cell4);
                row.appendChild(cell5);
                opponents_table.appendChild(row);

                // Mobile opponents table
                let mobile_row = document.createElement("tr");
                let mobile_cell1 = document.createElement("td");
                let mobile_cell2 = document.createElement("td");
                let mobile_cell3 = document.createElement("td");
                let mobile_cell4 = document.createElement("td");
                let mobile_cell5 = document.createElement("td");
                mobile_cell1.innerHTML = opponent.name;
                mobile_cell2.innerHTML = opponent.games_played_vs;
                mobile_cell3.innerHTML = opponent.wins_vs;
                mobile_cell4.innerHTML = opponent.losses_vs;
                mobile_cell5.innerHTML = (opponent.win_rate_vs * 100).toFixed(0) + "%";
                mobile_row.appendChild(mobile_cell1);
                mobile_row.appendChild(mobile_cell2);
                mobile_row.appendChild(mobile_cell3);
                mobile_row.appendChild(mobile_cell4);
                mobile_row.appendChild(mobile_cell5);
                opponents_table_mobile.appendChild(mobile_row);
            }
        });

    fetch(`https://api.scryfall.com/cards/named?exact=${selected_deck.split(" ").join("+")}`)
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
};

// Elo Records
fetch('/records')
    .then(response => response.json())
    .then(data => {
        console.log("ELO Records data:", data);
        let table = document.getElementById("elo_records");
        let row = table.insertRow();
        let cell1 = row.insertCell(0);
        let cell2 = row.insertCell(1);
        let cell3 = row.insertCell(2);
        let cell4 = row.insertCell(3);
        cell1.innerHTML = "Highest Current ELO";
        cell2.innerHTML = data.highest_current.deck;
        cell3.innerHTML = data.highest_current.elo_entry.elo.toFixed();
        cell4.innerHTML = `${data.highest_current.elo_entry.date}<br>ID: ${data.highest_current.elo_entry.game_id}`;

        row = table.insertRow();
        cell1 = row.insertCell(0);
        cell2 = row.insertCell(1);
        cell3 = row.insertCell(2);
        cell4 = row.insertCell(3);
        cell1.innerHTML = "Lowest Current ELO";
        cell2.innerHTML = data.lowest_current.deck;
        cell3.innerHTML = data.lowest_current.elo_entry.elo.toFixed()
        cell4.innerHTML = `${data.lowest_current.elo_entry.date}<br>ID: ${data.lowest_current.elo_entry.game_id}`;

        row = table.insertRow();
        cell1 = row.insertCell(0);
        cell2 = row.insertCell(1);
        cell3 = row.insertCell(2);
        cell4 = row.insertCell(3);
        cell1.innerHTML = "Highest ELO Ever";
        cell2.innerHTML = data.highest_ever.deck;
        cell3.innerHTML = data.highest_ever.elo_entry.elo.toFixed();
        cell4.innerHTML = `${data.highest_ever.elo_entry.date}<br>ID: ${data.highest_ever.elo_entry.game_id}`;

        row = table.insertRow();
        cell1 = row.insertCell(0);
        cell2 = row.insertCell(1);
        cell3 = row.insertCell(2);
        cell4 = row.insertCell(3);
        cell1.innerHTML = "Lowest ELO Ever";
        cell2.innerHTML = data.lowest_ever.deck;
        cell3.innerHTML = data.lowest_ever.elo_entry.elo.toFixed();
        cell4.innerHTML = `${data.lowest_ever.elo_entry.date}<br>ID: ${data.lowest_ever.elo_entry.game_id}`;

        // Mobile data
        document.getElementById("highest_current_elo").innerHTML = data.highest_current.deck + " (" + data.highest_current.elo_entry.elo.toFixed() + ")";
        document.getElementById("lowest_current_elo").innerHTML = data.lowest_current.deck + " (" + data.lowest_current.elo_entry.elo.toFixed() + ")";
        document.getElementById("highest_elo_ever").innerHTML = data.highest_ever.deck + " (" + data.highest_ever.elo_entry.elo.toFixed() + ")";
        document.getElementById("lowest_elo_ever").innerHTML = data.lowest_ever.deck + " (" + data.lowest_ever.elo_entry.elo.toFixed() + ")";

    });