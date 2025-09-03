import main

main.calculate_elos()

selected_deck = main.user_select_deck("Enter the name of the deck you would like to analyze matchups for:\n")

matchups = []
for deck in main.all_decks:
    if deck != selected_deck:
        elo_diff =  deck.get_current_elo() - selected_deck.get_current_elo()
        matchups.append((deck.name, elo_diff))

matchups.sort(key=lambda x: abs(x[1]))
print(f"\nTop 5 closest elo ratings for {selected_deck.name}:")
for i in range(min(5, len(matchups))):
    opponent, diff = matchups[i]
    print(f"{diff:>+7.2f} - {opponent}")
