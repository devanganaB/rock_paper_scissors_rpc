# client.py
import xmlrpc.client
import sys

def display_menu():
    """Display menu options"""
    print("\n===== Rock Paper Scissors Game =====")
    print("1. Register as a player")
    print("2. Play a round")
    print("3. View your score")
    print("4. View all players and scores")
    print("5. View game history")
    print("6. Exit")
    print("===================================")

def main():
    """Main client function"""
    # Connect to the XML-RPC server
    try:
        server = xmlrpc.client.ServerProxy('http://localhost:8000')
        print("Connected to the RPS game server")
    except Exception as e:
        print(f"Error connecting to server: {e}")
        sys.exit(1)
    
    player_name = None
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ")
        
        if choice == '1':
            if player_name:
                print(f"You are already registered as {player_name}")
            else:
                player_name = input("Enter your player name: ")
                result = server.register_player(player_name)
                print(result)
        
        elif choice == '2':
            if not player_name:
                print("Please register as a player first!")
                continue
            
            print("\nChoose: rock, paper, or scissors")
            player_choice = input("Your choice: ").lower()
            
            try:
                result = server.play(player_name, player_choice)
                print(result)
            except Exception as e:
                print(f"Error playing game: {e}")
        
        elif choice == '3':
            if not player_name:
                print("Please register as a player first!")
                continue
            
            try:
                score = server.get_score(player_name)
                print(score)
            except Exception as e:
                print(f"Error getting score: {e}")
        
        elif choice == '4':
            try:
                scores = server.get_all_scores()
                print("\n----- Player Scores -----")
                for p, s in scores.items():
                    print(f"{p}: {s}")
                print("------------------------")
            except Exception as e:
                print(f"Error getting scores: {e}")
        
        elif choice == '5':
            try:
                history = server.get_game_history()
                print("\n----- Game History -----")
                for i, game in enumerate(history, 1):
                    print(f"Game {i}:")
                    print(f"  Player: {game['player']}")
                    print(f"  Player's choice: {game['player_choice']}")
                    print(f"  Computer's choice: {game['computer_choice']}")
                    print(f"  Result: {game['result']}")
                    print("------------------------")
            except Exception as e:
                print(f"Error getting game history: {e}")
        
        elif choice == '6':
            print("Thank you for playing! Goodbye.")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()