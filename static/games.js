console.log("Populating games table...");

fetch('/get_all_games')
    .then(response => response.json())
    .then(data => {
        const table = document.getElementById("games_table");
        data.sort((a, b) => b.game_id - a.game_id).forEach(game => {
            // Populate table rows
            const row = table.insertRow();
            const cell1 = row.insertCell(0);
            const cell2 = row.insertCell(1);
            const cell3 = row.insertCell(2);
            const cell4 = row.insertCell(3);
            const cell5 = row.insertCell(4);
            const cell6 = row.insertCell(5);
            const cell7 = row.insertCell(6);
            cell1.innerHTML = game.game_id;
            cell2.innerHTML = game.winning_player;
            cell3.innerHTML = game.losing_players.join(", ");
            cell4.innerHTML = `${game.winning_deck.name}<br>(${Math.round(game.winning_deck.elo_before)} → ${Math.round(game.winning_deck.elo_after)})`;
            cell5.innerHTML = game.losing_decks.map(deck => `${deck.name}<br>(${Math.round(deck.elo_before)} → ${Math.round(deck.elo_after)})`).join("<br><br>");
            cell6.innerHTML = game.date;
            cell7.innerHTML = game.notes;

            // Populate game list for small screens.
            const gameList = document.getElementById("games_list");
            const listItem = document.createElement("div");
            listItem.className = "card";
            listItem.innerHTML = generateGameCard(game);
            gameList.appendChild(listItem);
        });
    });

document.getElementById("refresh_games_button").addEventListener("click", () => {
    document.querySelectorAll('.please_wait').forEach(el => {
        el.style.display = 'flex';
    });
    fetch('/update').then(() => {
        location.reload();
    }); 
});