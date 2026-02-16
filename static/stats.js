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

            document.getElementById("deck_name").innerHTML = data.deck_name;
            document.getElementById("deck_win_rate").innerHTML = (data.win_rate * 100).toFixed(2) + "%";
            document.getElementById("deck_elo").innerHTML = data.current_elo.toFixed(0);
            document.getElementById("deck_avrg_opponent_elo").innerHTML = data.avrg_opponent_elo.toFixed(2);
            document.getElementById("deck_avrg_opponent_elo_when_win").innerHTML = data.avrg_opponent_elo_when_win.toFixed(2);
            document.getElementById("deck_avrg_opponent_elo_when_lose").innerHTML = data.avrg_opponent_elo_when_lose.toFixed(2);
            document.getElementById("deck_most_common_opponents").innerHTML = data.most_common_opponents.map(opponent => `${opponent[0]} (${opponent[1]})`).join("<br>");
            document.getElementById("deck_win_rate_per_opponent").innerHTML = data.most_common_opponents_when_win.map(opponent => `${opponent[0]} (${opponent[1]}/${opponent[2]} - ${(opponent[1] / opponent[2] * 100).toFixed(0)}%)`).join("<br>");
            document.getElementById("deck_lose_rate_per_opponent").innerHTML = data.most_common_opponents_when_lose.map(opponent => `${opponent[0]} (${opponent[1]}/${opponent[2]} - ${(opponent[1] / opponent[2] * 100).toFixed(0)}%)`).join("<br>");
        });
}

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
        cell1.innerHTML = "Highest Current ELO";
        cell2.innerHTML = data.highest_current.deck;
        cell3.innerHTML = data.highest_current.elo.toFixed();

        row = table.insertRow();
        cell1 = row.insertCell(0);
        cell2 = row.insertCell(1);
        cell3 = row.insertCell(2);
        cell1.innerHTML = "Lowest Current ELO";
        cell2.innerHTML = data.lowest_current.deck;
        cell3.innerHTML = data.lowest_current.elo.toFixed();

        row = table.insertRow();
        cell1 = row.insertCell(0);
        cell2 = row.insertCell(1);
        cell3 = row.insertCell(2);
        cell1.innerHTML = "Highest Historical ELO";
        cell2.innerHTML = data.highest_historical.deck;
        cell3.innerHTML = data.highest_historical.elo.toFixed();

        row = table.insertRow();
        cell1 = row.insertCell(0);
        cell2 = row.insertCell(1);
        cell3 = row.insertCell(2);
        cell1.innerHTML = "Lowest Historical ELO";
        cell2.innerHTML = data.lowest_historical.deck;
        cell3.innerHTML = data.lowest_historical.elo.toFixed();
        });