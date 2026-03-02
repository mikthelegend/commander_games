fetch('/get_all_games')
    .then(response => response.json())
    .then(data => {
        data.sort((a, b) => b.game_id - a.game_id).forEach(game => {

            // Populate game list
            const gameList = document.getElementById("games_list");
            const listItem = generateGameCard(game);
            gameList.appendChild(listItem);
        });

        document.getElementById('game_id_display').value = Number(data[0].game_id) + 1;
    });

document.getElementById("refresh_games_button").addEventListener("click", () => {
    document.querySelectorAll('.please_wait').forEach(el => {
        el.style.display = 'flex';
    });
    fetch('/update').then(() => {
        location.reload();
    }); 
});

const new_game_button = document.getElementById('add_new_game_button');

new_game_button.addEventListener('click', () => {
    document.getElementById('input_game_details').style.display = 'block';
    document.getElementById('date_input').valueAsDate = new Date();
    console.log("New game form displayed");
});
