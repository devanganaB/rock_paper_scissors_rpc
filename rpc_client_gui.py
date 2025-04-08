# client_gui.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import xmlrpc.client
import threading
import time

class RPSGameClient(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Connect to the XML-RPC server
        try:
            self.server = xmlrpc.client.ServerProxy('http://localhost:8000')
            print("Connected to the RPS game server")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Error connecting to server: {e}")
            self.destroy()
            return
        
        # Game variables
        self.player_name = None
        self.is_registered = False
        
        # Setup the UI
        self.setup_ui()
    
    def setup_ui(self):
        # Configure the main window
        self.title("Rock Paper Scissors Game")
        self.geometry("800x600")
        self.resizable(True, True)
        
        # Create tabs
        self.tab_control = ttk.Notebook(self)
        
        # Login tab
        self.login_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.login_tab, text="Login")
        self.setup_login_tab()
        
        # Game tab
        self.game_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.game_tab, text="Play Game")
        self.setup_game_tab()
        
        # Scores tab
        self.scores_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.scores_tab, text="Scores")
        self.setup_scores_tab()
        
        # History tab
        self.history_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.history_tab, text="Game History")
        self.setup_history_tab()
        
        self.tab_control.pack(expand=1, fill="both")
        
        # Start the UI refresh thread
        self.should_refresh = True
        self.refresh_thread = threading.Thread(target=self.auto_refresh, daemon=True)
        self.refresh_thread.start()
    
    def setup_login_tab(self):
        # Create a frame for login
        login_frame = ttk.LabelFrame(self.login_tab, text="Player Registration")
        login_frame.pack(pady=50, padx=50, fill="both", expand=True)
        
        # Username field
        ttk.Label(login_frame, text="Player Name:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.username_entry = ttk.Entry(login_frame, width=30)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # Register button
        register_btn = ttk.Button(login_frame, text="Register", command=self.register_player)
        register_btn.grid(row=1, column=0, columnspan=2, pady=20)
        
        # Status label
        self.login_status = ttk.Label(login_frame, text="Not registered")
        self.login_status.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Players list
        ttk.Label(login_frame, text="Registered Players:").grid(row=3, column=0, padx=10, pady=(20, 10), sticky="w")
        self.players_listbox = tk.Listbox(login_frame, width=40, height=10)
        self.players_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        
        # Refresh button
        refresh_btn = ttk.Button(login_frame, text="Refresh Players", command=self.refresh_players)
        refresh_btn.grid(row=5, column=0, columnspan=2, pady=10)
    
    def setup_game_tab(self):
        # Create a frame for the game
        game_frame = ttk.LabelFrame(self.game_tab, text="Play Rock Paper Scissors")
        game_frame.pack(pady=20, padx=50, fill="both", expand=True)
        
        # Player info
        self.player_info_label = ttk.Label(game_frame, text="Not logged in")
        self.player_info_label.pack(pady=(20, 30))
        
        # Game choices
        choices_frame = ttk.Frame(game_frame)
        choices_frame.pack(pady=20)
        
        # Load images for rock, paper, scissors
        self.rock_img = tk.PhotoImage(data='''
            R0lGODlhPAA8AIAAAP///wAAACH5BAEAAAAALAAAAABAADQAAAJihI+py+0Po5y02ouz3rz7D4biSJbmiabqyrbuC8fyTNf2jef6zvf+DwwKh8Si8YhMKpfMpvMJjUqn1Kr1is1qt9yu9wsOi8fksvmMTqvX7Lb7DY/L5/S6/Y7P6/f8vv8vKgAAOw==
        ''')
        self.paper_img = tk.PhotoImage(data='''
            R0lGODlhPAA8AIAAAP///wAAACH5BAEAAAAALAAAAABAADQAAAJihI+py+0Po5y02ouz3rz7D4biSJbmiabqyrbuC8fyTNf2jef6zvf+DwwKh8Si8YhMKpfMpvMJjUqn1Kr1is1qt9yu9wsOi8fksvmMTqvX7Lb7DY/L5/S6/Y7P6/f8vv8vKgAAOw==
        ''')
        self.scissors_img = tk.PhotoImage(data='''
            R0lGODlhPAA8AIAAAP///wAAACH5BAEAAAAALAAAAABAADQAAAJihI+py+0Po5y02ouz3rz7D4biSJbmiabqyrbuC8fyTNf2jef6zvf+DwwKh8Si8YhMKpfMpvMJjUqn1Kr1is1qt9yu9wsOi8fksvmMTqvX7Lb7DY/L5/S6/Y7P6/f8vv8vKgAAOw==
        ''')
        
        # Create game choice buttons
        rock_btn = ttk.Button(choices_frame, text="Rock", width=20, 
                              command=lambda: self.play_game("rock"))
        rock_btn.grid(row=0, column=0, padx=10, pady=10)
        
        paper_btn = ttk.Button(choices_frame, text="Paper", width=20,
                              command=lambda: self.play_game("paper"))
        paper_btn.grid(row=0, column=1, padx=10, pady=10)
        
        scissors_btn = ttk.Button(choices_frame, text="Scissors", width=20,
                                command=lambda: self.play_game("scissors"))
        scissors_btn.grid(row=0, column=2, padx=10, pady=10)
        
        # Game results
        result_frame = ttk.LabelFrame(game_frame, text="Game Results")
        result_frame.pack(pady=20, fill="both", expand=True)
        
        # Player choice
        self.player_choice_label = ttk.Label(result_frame, text="Your choice: ")
        self.player_choice_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Computer choice
        self.computer_choice_label = ttk.Label(result_frame, text="Computer choice: ")
        self.computer_choice_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        # Game result
        self.game_result_label = ttk.Label(result_frame, text="Result: ")
        self.game_result_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        
        # Current score
        self.player_score_label = ttk.Label(result_frame, text="Your score: 0")
        self.player_score_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    
    def setup_scores_tab(self):
        # Create a frame for scores
        scores_frame = ttk.LabelFrame(self.scores_tab, text="Player Scores")
        scores_frame.pack(pady=20, padx=50, fill="both", expand=True)
        
        # Scores tree view
        columns = ('player', 'score')
        self.scores_tree = ttk.Treeview(scores_frame, columns=columns, show='headings')
        self.scores_tree.heading('player', text='Player')
        self.scores_tree.heading('score', text='Score')
        self.scores_tree.column('player', width=200)
        self.scores_tree.column('score', width=100)
        self.scores_tree.pack(pady=10, fill="both", expand=True)
        
        # Refresh button
        refresh_btn = ttk.Button(scores_frame, text="Refresh Scores", command=self.refresh_scores)
        refresh_btn.pack(pady=10)
    
    def setup_history_tab(self):
        # Create a frame for history
        history_frame = ttk.LabelFrame(self.history_tab, text="Game History")
        history_frame.pack(pady=20, padx=50, fill="both", expand=True)
        
        # History text area
        self.history_text = scrolledtext.ScrolledText(history_frame, width=70, height=20)
        self.history_text.pack(pady=10, fill="both", expand=True)
        
        # Refresh button
        refresh_btn = ttk.Button(history_frame, text="Refresh History", command=self.refresh_history)
        refresh_btn.pack(pady=10)
    
    def register_player(self):
        player_name = self.username_entry.get().strip()
        if not player_name:
            messagebox.showwarning("Input Error", "Please enter a player name")
            return
        
        try:
            result = self.server.register_player(player_name)
            self.login_status.config(text=result)
            
            if "already exists" not in result:
                self.player_name = player_name
                self.is_registered = True
                self.player_info_label.config(text=f"Playing as: {player_name}")
                
                # Switch to the game tab
                self.tab_control.select(1)
            
            # Refresh the players list
            self.refresh_players()
            
        except Exception as e:
            messagebox.showerror("Server Error", f"Error registering player: {e}")
    
    def refresh_players(self):
        try:
            players = self.server.get_all_players()
            self.players_listbox.delete(0, tk.END)  # Clear listbox
            
            for player in players:
                self.players_listbox.insert(tk.END, player)
        except Exception as e:
            messagebox.showerror("Server Error", f"Error getting players: {e}")
    
    def play_game(self, choice):
        if not self.is_registered:
            messagebox.showwarning("Authentication Required", "Please register first")
            self.tab_control.select(0)  # Switch to login tab
            return
        
        try:
            result = self.server.play(self.player_name, choice)
            
            # Update result labels
            self.player_choice_label.config(text=f"Your choice: {choice}")
            
            # Extract computer choice and result from the returned string
            # String format: "You chose rock, computer chose paper. Computer wins!"
            parts = result.split(", ")
            computer_choice = parts[1].split(" ")[2]
            game_result = parts[1].split(".")[1].strip()
            
            self.computer_choice_label.config(text=f"Computer choice: {computer_choice}")
            self.game_result_label.config(text=f"Result: {game_result}")
            
            # Update score
            self.update_player_score()
            
            # Refresh scores and history
            self.refresh_scores()
            self.refresh_history()
            
        except Exception as e:
            messagebox.showerror("Game Error", f"Error playing game: {e}")
    
    def update_player_score(self):
        try:
            score_text = self.server.get_score(self.player_name)
            # Extract score value from format: "player's score: 3"
            score = score_text.split(":")[1].strip()
            self.player_score_label.config(text=f"Your score: {score}")
        except Exception as e:
            print(f"Error updating score: {e}")
    
    def refresh_scores(self):
        try:
            scores = self.server.get_all_scores()
            
            # Clear current items
            for i in self.scores_tree.get_children():
                self.scores_tree.delete(i)
            
            # Add new scores
            for player, score in scores.items():
                self.scores_tree.insert('', tk.END, values=(player, score))
                
        except Exception as e:
            print(f"Error refreshing scores: {e}")
    
    def refresh_history(self):
        try:
            history = self.server.get_game_history()
            
            # Clear current text
            self.history_text.delete(1.0, tk.END)
            
            if not history:
                self.history_text.insert(tk.END, "No games played yet.")
                return
            
            # Add history entries
            for i, game in enumerate(history, 1):
                entry = f"Game {i}:\n"
                entry += f"  Player: {game['player']}\n"
                entry += f"  Player's choice: {game['player_choice']}\n"
                entry += f"  Computer's choice: {game['computer_choice']}\n"
                entry += f"  Result: {game['result']}\n"
                entry += "-" * 50 + "\n"
                
                self.history_text.insert(tk.END, entry)
                
        except Exception as e:
            print(f"Error refreshing history: {e}")
    
    def auto_refresh(self):
        """Auto refresh scores and players every few seconds"""
        while self.should_refresh:
            if self.is_registered:
                self.update_player_score()
                self.refresh_scores()
            self.refresh_players()
            time.sleep(5)  # Refresh every 5 seconds
    
    def on_closing(self):
        """Handle window closing"""
        self.should_refresh = False
        if self.refresh_thread.is_alive():
            self.refresh_thread.join(1)  # Wait for thread to finish
        self.destroy()

if __name__ == "__main__":
    app = RPSGameClient()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()