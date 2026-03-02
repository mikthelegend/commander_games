function loadRandomGames() {
    fetch('/get_all_games')
        .then(response => response.json())
        .then(data => {
            const random_indexes = [];
            while (random_indexes.length < 3 && random_indexes.length < data.length) {
                const random_index = Math.floor(Math.random() * data.length);
                if (!random_indexes.includes(random_index)) {
                    random_indexes.push(random_index);
                }
            }

            const random_games = random_indexes.map(index => data[index]);
            
            // After fetching the random games, populate the cards
            const container = document.getElementById('random_games_container');
            container.innerHTML = '';
            random_games.forEach(random_game => {
                const randomGameCard = generateGameCard(random_game);
                container.appendChild(randomGameCard);
            });
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

document.addEventListener('DOMContentLoaded', function() {
    loadRandomGames();
});

document.getElementById('new_random_game_btn').addEventListener('click', function() {
    loadRandomGames();
});
