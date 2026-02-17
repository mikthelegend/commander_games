
const new_game_button = document.getElementById('add_new_game_button');

new_game_button.addEventListener('click', () => {
    document.getElementById('add_new_game_card').style.display = 'block';
    document.getElementById('date_input').valueAsDate = new Date();
    console.log("New game form displayed");
});

const losersContainer = document.getElementById('losers');
const addBtn = document.getElementById('add-loser');
const remBtn = document.getElementById('remove-loser');

// Add event listener to the "Add Loser" button
addBtn.addEventListener('click', () => {
    const new_loser_row = losersContainer.firstElementChild.cloneNode(true);

    new_loser_row.querySelectorAll('select').forEach(select => {
        select.value = '';
    });

    losersContainer.appendChild(new_loser_row);
});

// Add event listener to the "Remove Loser" button
remBtn.addEventListener('click', () => {
    const rows = losersContainer.getElementsByClassName('player-deck-row');
    if (rows.length > 1) {
        losersContainer.removeChild(rows[rows.length - 1]);
    }
});

cancelBtn = document.getElementById('cancel_new_game');
cancelBtn.addEventListener('click', () => {
    document.getElementById('add_new_game_card').style.display = 'none';
});

// Fetch players and decks to populate the dropdowns
fetch('/get_all_players')
    .then(response => response.json())
    .then(data => {
        const playerSelects = document.querySelectorAll('.player_select');
        playerSelects.forEach(select => {
            data.forEach(player => {
                const option = document.createElement('option');
                option.value = player;
                option.textContent = player;
                select.appendChild(option);
            });
        });
    });

fetch('/get_all_decks')
    .then(response => response.json())
    .then(data => {
        const deckSelects = document.querySelectorAll('.deck_select');
        deckSelects.forEach(select => {
            data.forEach(deck => {
                const option = document.createElement('option');
                option.value = deck.name;
                option.textContent = deck.name;
                select.appendChild(option);
            });
        });
    });

// Handle form submission
const formElement = document.getElementById('new_game_form')
formElement.addEventListener('submit', function (event) {
    event.preventDefault();
    document.querySelectorAll('.please_wait').forEach(el => {
        el.style.display = 'flex';
    });

    const formData = new FormData(formElement);
    const data = {};

    // Convert FormData to a regular object, handling multiple values for the same key
    formData.forEach((value, key) => {
        if (key.endsWith('[]')) {
            const actualKey = key.slice(0, -2);
            if (!data[actualKey]) {
                data[actualKey] = [];
            }
            data[actualKey].push(value);
        } else {
            data[key] = value;
        }
    });

    console.log('Submitting form data:', data);
    fetch(formElement.action, {
        method: formElement.method,
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(result => {
            console.log('Success:', result);
            formElement.reset();
            location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
        });
});