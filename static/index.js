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
            document.getElementById('random_games_container').innerHTML = '';
            random_games.forEach(random_game => {
                const randomGameCard = document.createElement('div');
                randomGameCard.className = 'game-card';
                randomGameCard.innerHTML = `<strong>Game ID:</strong> ${random_game.game_id} <strong>Date:</strong> ${random_game.date} <br>
                                            <strong>Winner:</strong> ${random_game.winning_player} <br>(${random_game.winning_deck}) <br>
                                            <strong>Losers:</strong> ${random_game.losing_players.join(", ")} <br>
                                            <strong>Losing Decks:</strong> <br>${random_game.losing_decks.join("<br>")} <br>
                                            <strong>Notes:</strong> <br>${random_game.notes}`;

                document.getElementById('random_games_container').appendChild(randomGameCard);
            });
        });
}

document.addEventListener('DOMContentLoaded', function() {
    loadRandomGames();
});

document.getElementById('new_random_game_btn').addEventListener('click', function() {
    loadRandomGames();
});
