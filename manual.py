import main

main.calculate_elos()
main.update_spreadsheet()

# for deck in main.all_decks:
#     print(f"{deck['deck_name']}:")
#     for elo in deck['elos']:
#         print(f"  Elo: {elo['elo']}, Date: {elo['date']}")