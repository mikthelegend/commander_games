const gameId = document.getElementById("game_id").textContent.split(":")[1].trim();

document.getElementById("back_to_games_button").addEventListener("click", () => {
    location.href = "/games";
});

document.getElementById("edit_game_button").addEventListener("click", () => {
    document.getElementById("input_game_details").style.display = "block";
    document.getElementById("view_game_block").style.display = "none";

    fetch(`/get_game/${gameId}`)
        .then(response => response.json())
        .then(game => {
            console.log("Populating edit form with game data");
            
            console.log(game);

            const day = game.date.split("/")[0].padStart(2, '0');
            const month = game.date.split("/")[1].padStart(2, '0');
            const year = "20" + game.date.split("/")[2];


            document.getElementById("date_input").value = `${year}-${month}-${day}`;
            document.getElementById('game_id_display').value = game.game_id;
            document.getElementsByName("winning_player")[0].value = game.winner.pilot;
            document.getElementsByName("winning_deck")[0].value = game.winner.deck_name;
            document.getElementsByName("notes")[0].value = game.notes;

            const num_losers = game.losers.length;
            for (let i = 1; i < num_losers; i++) {
                addLoserRow();
            }

            document.getElementById("losers").querySelectorAll('.player-deck-row').forEach((row, index) => {
                if (index < num_losers) {
                    row.querySelector('select[name="losing_players[]"]').value = game.losers[index].pilot;
                    row.querySelector('select[name="losing_decks[]"]').value = game.losers[index].deck_name;
                }
            });
        });
})

document.getElementById("delete_game_button").addEventListener("click", () => {
    if (confirm("Are you sure you want to delete this game? This action cannot be undone.")) {
        document.querySelectorAll('.please_wait').forEach(el => {
            el.style.display = 'flex';
        });
        fetch(`/delete_game/${gameId}`, { method: 'DELETE' })
            .then(response => {
                if (response.ok) {
                    alert("Game deleted successfully.");
                    location.href = "/games";
                } else {
                    alert("Failed to delete game.");
                    location.reload();
                }
            });
    }
});