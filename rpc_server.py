# server.py
import random
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import threading

# Define the request handler class
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Game state
player_scores = {}
game_history = []

class RPSGame:
    def __init__(self):
        self.choices = ["rock", "paper", "scissors"]
    
    def register_player(self, player_name):
        """Register a new player for the game"""
        if player_name not in player_scores:
            player_scores[player_name] = 0
            return f"Player {player_name} registered successfully!"
        return f"Player {player_name} already exists!"
    
    def get_all_players(self):
        """Get a list of all registered players"""
        return list(player_scores.keys())
    
    def play(self, player_name, player_choice):
        """Play a round of rock paper scissors"""
        if player_name not in player_scores:
            return f"Player {player_name} not registered! Please register first."
        
        player_choice = player_choice.lower()
        if player_choice not in self.choices:
            return f"Invalid choice! Please choose from {self.choices}"
        
        # Computer makes a random choice
        computer_choice = random.choice(self.choices)
        
        # Determine the winner
        result = self._determine_winner(player_choice, computer_choice)
        
        # Update scores
        if "win" in result:
            player_scores[player_name] += 1
        
        # Add to game history
        game_history.append({
            "player": player_name,
            "player_choice": player_choice,
            "computer_choice": computer_choice,
            "result": result
        })
        
        return f"You chose {player_choice}, computer chose {computer_choice}. {result}"
    
    def _determine_winner(self, player_choice, computer_choice):
        """Determine the winner based on the choices"""
        if player_choice == computer_choice:
            return "It's a tie!"
        
        if (player_choice == "rock" and computer_choice == "scissors") or \
           (player_choice == "paper" and computer_choice == "rock") or \
           (player_choice == "scissors" and computer_choice == "paper"):
            return "You win!"
        else:
            return "Computer wins!"
    
    def get_score(self, player_name):
        """Get the score for a specific player"""
        if player_name not in player_scores:
            return f"Player {player_name} not registered!"
        return f"{player_name}'s score: {player_scores[player_name]}"
    
    def get_all_scores(self):
        """Get scores for all players"""
        return player_scores
    
    def get_game_history(self):
        """Get the history of all games played"""
        return game_history
    
    def reset_scores(self):
        """Reset all scores to zero"""
        for player in player_scores:
            player_scores[player] = 0
        return "All scores have been reset"
    
    def reset_game_history(self):
        """Reset game history"""
        global game_history
        game_history = []
        return "Game history has been cleared"

# Create server
def start_server(host="localhost", port=8000):
    # Create server
    server = SimpleXMLRPCServer((host, port), 
                                requestHandler=RequestHandler,
                                allow_none=True)
    server.register_introspection_functions()
    
    # Register game instance
    game = RPSGame()
    server.register_instance(game)
    
    # Start the server
    print(f"Starting RPC server on {host}:{port}...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Exiting server...")

if __name__ == "__main__":
    # start_server()
    # Start the server in a thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    
    print("Server is running. Press Enter to stop.")
    input()  # Wait for Enter key to stop the server
    print("Server stopped.")