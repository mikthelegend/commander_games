console.log("Populating deck dropdown...");

// Matchup generation

let innerHTML = "";
fetch('/get_all_decks')
    .then(response => response.json())
    .then(data => {
        data.forEach(deck => {
            innerHTML += `<option value="${deck.name}">${deck.name}</option>`;
        });
        document.getElementById("matchup_dropdown").innerHTML = innerHTML;
    });

document.getElementById("matchup_button").onclick = function() {
    let selected_deck = document.getElementById("matchup_dropdown").value;
    console.log("Selected deck:", selected_deck);
    fetch(`/matchup?deck_name=${encodeURIComponent(selected_deck)}`)
        .then(response => response.json())
        .then(data => {
            const table = document.getElementById("matchup_result");
            // Clear previous results
            table.innerHTML = `<tr>
                    <th>Deck Name</th>
                    <th>ELO Difference</th>
                </tr>`;
            for (let i = 0; i < Math.min(5, data.length); i++) {
                const entry = data[i];
                const opponent = entry[0];
                const elo_diff = entry[1];
                const row = table.insertRow();
                const cell1 = row.insertCell(0);
                const cell2 = row.insertCell(1);
                cell1.innerHTML = opponent;
                cell2.innerHTML = (elo_diff<0?"":"+") + String(elo_diff.toFixed(2));
                cell2.style.color = elo_diff < 0 ? "red" : "green";
            }
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