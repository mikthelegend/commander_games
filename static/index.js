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
        document.getElementById('highest_current_elo_deck_name').innerHTML += data.highest_current.deck;
        document.getElementById('highest_current_elo').innerHTML += data.highest_current.elo_entry.elo.toFixed(0);
        document.getElementById('highest_current_elo_when').innerHTML += `${data.highest_current.elo_entry.date} (Game ID: ${data.highest_current.elo_entry.game_id})`;

        document.getElementById('lowest_current_elo_deck_name').innerHTML += data.lowest_current.deck;
        document.getElementById('lowest_current_elo').innerHTML += data.lowest_current.elo_entry.elo.toFixed(0);
        document.getElementById('lowest_current_elo_when').innerHTML += `${data.lowest_current.elo_entry.date} (Game ID: ${data.lowest_current.elo_entry.game_id})`;

        document.getElementById('highest_all_time_elo_deck_name').innerHTML += data.highest_ever.deck;
        document.getElementById('highest_all_time_elo').innerHTML += data.highest_ever.elo_entry.elo.toFixed(0);
        document.getElementById('highest_all_time_elo_when').innerHTML += `${data.highest_ever.elo_entry.date} (Game ID: ${data.highest_ever.elo_entry.game_id})`;

        document.getElementById('lowest_all_time_elo_deck_name').innerHTML += data.lowest_ever.deck;
        document.getElementById('lowest_all_time_elo').innerHTML += data.lowest_ever.elo_entry.elo.toFixed(0);
        document.getElementById('lowest_all_time_elo_when').innerHTML += `${data.lowest_ever.elo_entry.date} (Game ID: ${data.lowest_ever.elo_entry.game_id})`;

        fetch(`https://api.scryfall.com/cards/named?exact=${data.highest_current.deck.split(" ").join("+")}`)
            .then(response => response.json())
            .then(data => {
                console.log("Scryfall data:", data);
                if (data.image_uris && data.image_uris.normal) {
                    document.getElementById("highest_current_elo_deck_image").src = data.image_uris.normal;
                    document.getElementById("highest_current_elo_deck_image").style.display = "block";
                } else {
                    document.getElementById("highest_current_elo_deck_image").style.display = "none";
                }
            })

        fetch(`https://api.scryfall.com/cards/named?exact=${data.lowest_current.deck.split(" ").join("+")}`)
            .then(response => response.json())
            .then(data => {
                console.log("Scryfall data:", data);
                if (data.image_uris && data.image_uris.normal) {
                    document.getElementById("lowest_current_elo_deck_image").src = data.image_uris.normal;
                    document.getElementById("lowest_current_elo_deck_image").style.display = "block";
                } else {
                    document.getElementById("lowest_current_elo_deck_image").style.display = "none";
                }
            })

        fetch(`https://api.scryfall.com/cards/named?exact=${data.highest_ever.deck.split(" ").join("+")}`)
            .then(response => response.json())
            .then(data => {
                console.log("Scryfall data:", data);
                if (data.image_uris && data.image_uris.normal) {
                    document.getElementById("highest_all_time_elo_deck_image").src = data.image_uris.normal;
                    document.getElementById("highest_all_time_elo_deck_image").style.display = "block";
                } else {
                    document.getElementById("highest_all_time_elo_deck_image").style.display = "none";
                }
            })

        fetch(`https://api.scryfall.com/cards/named?exact=${data.lowest_ever.deck.split(" ").join("+")}`)
            .then(response => response.json())
            .then(data => {
                console.log("Scryfall data:", data);
                if (data.image_uris && data.image_uris.normal) {
                    document.getElementById("lowest_all_time_elo_deck_image").src = data.image_uris.normal;
                    document.getElementById("lowest_all_time_elo_deck_image").style.display = "block";
                } else {
                    document.getElementById("lowest_all_time_deck_image").style.display = "none";
                }
            })

    });

document.addEventListener('DOMContentLoaded', function() {
    loadRandomGames();
});

document.getElementById('new_random_game_btn').addEventListener('click', function() {
    loadRandomGames();
});
