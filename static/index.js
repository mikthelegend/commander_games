function loadRandomGame() {
    fetch('/get_all_games')
        .then(response => response.json())
        .then(data => {
            const random_game = data[Math.floor(Math.random() * data.length)];
            
            // After fetching the random game, populate the card
            const randomGameCard = document.getElementById('random_game')
            randomGameCard.innerHTML = `<strong>Game ID:</strong> ${random_game.game_id} <strong>Date:</strong> ${random_game.date} <br>
                                        <strong>Winner:</strong> ${random_game.winning_player} <br>(${random_game.winning_deck}) <br>
                                        <strong>Losers:</strong> ${random_game.losing_players.join(", ")} <br>
                                        <strong>Losing Decks:</strong> <br>${random_game.losing_decks.join("<br>")} <br>
                                        <strong>Notes:</strong> <br>${random_game.notes}`;
        });
    }

document.addEventListener('DOMContentLoaded', function() {
    loadRandomGame();
});

document.getElementById('new_random_game_btn').addEventListener('click', function() {
    loadRandomGame();
});
