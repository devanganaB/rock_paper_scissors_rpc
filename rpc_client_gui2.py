# client_gui.py
import xmlrpc.client
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
from datetime import datetime

class RPSClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors Game")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Connect to server
        try:
            self.server = xmlrpc.client.ServerProxy('http://localhost:8000')
            self.connection_status = "Connected to the RPS game server"
        except Exception as e:
            self.connection_status = f"Error connecting to server: {e}"
            messagebox.showerror("Connection Error", self.connection_status)
            sys.exit(1)
        
        self.player_name = None
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.home_tab = ttk.Frame(self.notebook)
        self.play_tab = ttk.Frame(self.notebook)
        self.scores_tab = ttk.Frame(self.notebook)
        self.history_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.home_tab, text="Home")
        self.notebook.add(self.play_tab, text="Play Game")
        self.notebook.add(self.scores_tab, text="Scores")
        self.notebook.add(self.history_tab, text="Game History")
        
        # Setup each tab
        self._setup_home_tab()
        self._setup_play_tab()
        self._setup_scores_tab()
        self._setup_history_tab()
        
        # Status bar at the bottom
        self.status_bar = tk.Label(root, text=self.connection_status, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Update status periodically
        self._update_status()
    
    def _setup_home_tab(self):
        # Welcome message
        frame = ttk.Frame(self.home_tab, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Welcome to Rock Paper Scissors Game", font=("Arial", 18)).pack(pady=20)
        
        # Connection info
        ttk.Label(frame, text=self.connection_status).pack(pady=5)
        
        # Registration section
        reg_frame = ttk.LabelFrame(frame, text="Player Registration", padding="10")
        reg_frame.pack(pady=20, fill=tk.X)
        
        ttk.Label(reg_frame, text="Enter your name:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.name_entry = ttk.Entry(reg_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.register_button = ttk.Button(reg_frame, text="Register", command=self._register_player)
        self.register_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Registration status
        self.reg_status = ttk.Label(reg_frame, text="")
        self.reg_status.grid(row=1, column=0, columnspan=3, pady=5)
        
        # Player info (shown after registration)
        self.player_info_frame = ttk.LabelFrame(frame, text="Player Information", padding="10")
        self.player_info_label = ttk.Label(self.player_info_frame, text="")
        self.player_info_label.pack(pady=5)
        
        # Instructions
        instr_frame = ttk.LabelFrame(frame, text="How to Play", padding="10")
        instr_frame.pack(pady=20, fill=tk.X)
        
        instructions = """
        1. Register as a player with your name
        2. Go to the 'Play Game' tab to play Rock, Paper, Scissors
        3. View your score and others' scores in the 'Scores' tab
        4. Check the game history in the 'Game History' tab
        """
        ttk.Label(instr_frame, text=instructions).pack(pady=5)
    
    def _setup_play_tab(self):
        frame = ttk.Frame(self.play_tab, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Play Rock Paper Scissors", font=("Arial", 16)).pack(pady=10)
        
        # Game choices
        choices_frame = ttk.Frame(frame)
        choices_frame.pack(pady=20)
        
        # Create images for buttons
        self.rock_img = tk.PhotoImage(data='''
            R0lGODlhQABAAOf/AAAAAAABAQECAgIDAwMEBAQFBQUGBgYHBwcICAgJCQkKCgoLCwsMDA
            wNDQ0ODg4PDw8QEBAREREPDxIQEBMREREUFBQVFRUWFhYXFxcYGBgZGRkaGhobGxscHBwd
            HR0eHh4fHx8gICAgICAhISEiIiIjIyMkJCQlJSUmJiYnJycoKCgpKSkqKiorKyssLCwtLS
            0uLi4vLy8wMDAxMTEyMjEzMzM0NDQ1NTU2NjY3Nzc4ODg5OTk6Ojo7Ozs8PDw9PT09fX19v
            b29/f3+Pj4+fn5+vr6+/v7/Pz8/f39/v7+////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AACH5BAEAAD8ALAAAAABAAEAAAAj+AH8IHEiwoMGDCBMqXMiwocOHEB1GnEixosWJFTNq3M
            ixo8ePDUOKHEmypMmTKFOqXMlypcuXMGPKnAlT5sqbOHPqLNkSYM+fQHsKHUq0qNGjSJMqXc
            q0qdOnUKNKnUq1qtWrWLNq3cq1q9evYMOKHUu2rNmzaNOqXcu2rdu3cOPKnUu3rt27ePPq3c
            u3r9+/gAMLHky4sOHDiBMrXsy4sePHkCNLnky5suXLmDNr3sy5s+fPoEOLHk26tOm9N1OrXs
            26tevXsBk2cE27tu3buHPr3s27t+/fwIMLH068uPHjyJMrX868ufPn0KNLn069uvXr2LNr36
            69NSD37+DDix9Pvrz58+jTq19/cmAA9vDjy59Pv779+/jz69/Pv7///wDyh58ABAYYIEC+HC
            jggAQWaOCBCCao4IIMNlgPA/xE2IpADla4SoYcdujhhyCGKOKIJJZo4okopqjiiiy26OKNMP
            boC0E01mjjjTjmqOOOPPbo449ABinkkEQWaeSRSCap5JJMNunkk1BGKeWUVFZp5ZVYZqnlll
            x26eWXYIYp5phklmnmmWimqeaabLbp5ptwxinnnHTWaeedeOap55589unnn4AGKuighBZq6KG
            IJqrooow2OlBAADs=
        ''')
        self.rock_img = self.rock_img.subsample(2, 2)  # Resize
        
        self.paper_img = tk.PhotoImage(data='''
            R0lGODlhQABAAOf/AAAAAAABAQECAgIDAwMEBAQFBQUGBgYHBwcICAgJCQkKCgoLCwsMDA
            wNDQ0ODg4PDw8QEBAREREPDxIQEBMREREUFBQVFRUWFhYXFxcYGBgZGRkaGhobGxscHBwd
            HR0eHh4fHx8gICAgICAhISEiIiIjIyMkJCQlJSUmJiYnJycoKCgpKSkqKiorKyssLCwtLS
            0uLi4vLy8wMDAxMTEyMjEzMzM0NDQ1NTU2NjY3Nzc4ODg5OTk6Ojo7Ozs8PDw9PT09fX19v
            b29/f3+Pj4+fn5+vr6+/v7/Pz8/f39/v7+////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AACH5BAEAAD8ALAAAAABAAEAAAAj+AH8IHEiwoMGDCBMqXMiwocOHEB1GnEixosWJFTNq3M
            ixo8ePDUOKHEmypMmTKFOqXMlypcuXMGPKnAlT5sqbOHPqLNkSYM+fQHsKHUq0qNGjSJMqXc
            q0qdOnUKNKnUq1qtWrWLNq3cq1q9evYMOKHUu2rNmzaNOqXcu2rdu3cOPKnUu3rt27ePPq3c
            u3r9+/gAMLHky4sOHDiBMrXsy4sePHkCNLnky5suXLmDNr3sy5s+fPoEOLHk26tOm9N1OrXs
            26tevXsBk2cE27tu3buHPr3s27t+/fwIMLH058IIbiyJMrX868ufPn0KNLn069uvXr2LNr36
            59+HTo0KeTNMm+YST59/Djy59Pv779+/jz69/Pv7///wAGKOCABBZo4IEIJqjgggw26OCDEEYo
            4YQUVmjhhRhmqOGGHHbo4YcghijiiCSWaOKJKKao4oostujii+nFKOOMNNZo44045qjjjjz26
            OOPQAYp5JBEFmnkkUgmqeSSTDbp5JNQRinllFRWaeWVWGap5ZZcdunll2CGKeaYZJZp5plopqn
            mmmy26eabcMYp55x01mnnnXjmqeeefPbp55+ABirooIQWauihiCaq6KKMNuroo5BGKumklFZq
            6aWYZqrpppx26umnoIYq6qg9BQQAOw==
        ''')
        self.paper_img = self.paper_img.subsample(2, 2)  # Resize
        
        self.scissors_img = tk.PhotoImage(data='''
            R0lGODlhQABAAOf/AAAAAAABAQECAgIDAwMEBAQFBQUGBgYHBwcICAgJCQkKCgoLCwsMDA
            wNDQ0ODg4PDw8QEBAREREPDxIQEBMREREUFBQVFRUWFhYXFxcYGBgZGRkaGhobGxscHBwd
            HR0eHh4fHx8gICAgICAhISEiIiIjIyMkJCQlJSUmJiYnJycoKCgpKSkqKiorKyssLCwtLS
            0uLi4vLy8wMDAxMTEyMjEzMzM0NDQ1NTU2NjY3Nzc4ODg5OTk6Ojo7Ozs8PDw9PT09fX19v
            b29/f3+Pj4+fn5+vr6+/v7/Pz8/f39/v7+////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AACH5BAEAAD8ALAAAAABAAEAAAAj+AH8IHEiwoMGDCBMqXMiwocOHEB1GnEixosWJFTNq3M
            ixo8ePDUOKHEmypMmTKFOqXMlypcuXMGPKnAlT5sqbOHPqLNkSYM+fQHsKHUq0qNGjSJMqXc
            q0qdOnUKNKnUq1qtWrWLNq3cq1q9evYMOKHUu2rNmzaNOqXcu2rdu3cOPKnUu3rt27ePPq3c
            u3r9+/gAMLHky4sOHDiBMrXsy4sePHkCNLnky5suXLmDNr3sy5s+fPoEOLHk26tOm9N1OrXs
            26tevXsBk2cE27tu3buHPr3s27t+/fwIMLH058IIbiyJMrX868ufPn0KNLn069uvXr2LNr36
            69+HTo0KeTNMm+YST59/Djy59Pv779+/jz69/Pv7///wAGKOCABBZo4IEIJqjgggw26OCDEEYo
            4WsVmHSCKBZkqOGGHHbo4YcghijiiCSWaOKJKKao4oostujii+HJKOOMNNZo44045qjjjjz26
            OOPQAYp5JBEFmnkkUgmqeSSTDbp5JNQRinllFRWaeWVWGap5ZZcdunll2CmFl9QhcVy45lopqn
            mmmy26eabcMYp55x01mnnnXjmqeeefPbp55+ABirooIQWauihiCaq6KKMNuroo5BGKumklFZq
            6aWYZqrpppx26umnoIYq6qikPhUQADs=
        ''')
        self.scissors_img = self.scissors_img.subsample(2, 2)  # Resize
        
        rock_btn = ttk.Button(choices_frame, image=self.rock_img, command=lambda: self._play_game("rock"))
        rock_btn.grid(row=0, column=0, padx=10, pady=10)
        ttk.Label(choices_frame, text="Rock").grid(row=1, column=0)
        
        paper_btn = ttk.Button(choices_frame, image=self.paper_img, command=lambda: self._play_game("paper"))
        paper_btn.grid(row=0, column=1, padx=10, pady=10)
        ttk.Label(choices_frame, text="Paper").grid(row=1, column=1)
        
        scissors_btn = ttk.Button(choices_frame, image=self.scissors_img, command=lambda: self._play_game("scissors"))
        scissors_btn.grid(row=0, column=2, padx=10, pady=10)
        ttk.Label(choices_frame, text="Scissors").grid(row=1, column=2)
        
        # Game result display
        result_frame = ttk.LabelFrame(frame, text="Game Results", padding="10")
        result_frame.pack(pady=20, fill=tk.X)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, width=60, height=10, wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        self.result_text.config(state=tk.DISABLED)
        
        # Clear results button
        ttk.Button(result_frame, text="Clear Results", command=self._clear_results).pack(pady=5)
    
    def _setup_scores_tab(self):
        frame = ttk.Frame(self.scores_tab, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Player Scores", font=("Arial", 16)).pack(pady=10)
        
        # Refresh and reset buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Refresh Scores", command=self._refresh_scores).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Reset All Scores", command=self._reset_scores).pack(side=tk.LEFT, padx=5)
        
        # Scores display
        scores_frame = ttk.LabelFrame(frame, text="Current Scores", padding="10")
        scores_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create treeview for scores
        columns = ("Player", "Score")
        self.scores_tree = ttk.Treeview(scores_frame, columns=columns, show="headings")
        
        # Define headings
        for col in columns:
            self.scores_tree.heading(col, text=col)
            self.scores_tree.column(col, width=150, anchor=tk.CENTER)
        
        self.scores_tree.pack(fill=tk.BOTH, expand=True)
        
        # Initial load of scores
        self._refresh_scores()
    
    def _setup_history_tab(self):
        frame = ttk.Frame(self.history_tab, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Game History", font=("Arial", 16)).pack(pady=10)
        
        # Refresh and reset buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Refresh History", command=self._refresh_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear History", command=self._clear_history).pack(side=tk.LEFT, padx=5)
        
        # History display
        history_frame = ttk.LabelFrame(frame, text="Game Records", padding="10")
        history_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create treeview for history
        columns = ("Game", "Player", "Player Choice", "Computer Choice", "Result")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings")
        
        # Define headings
        for col in columns:
            self.history_tree.heading(col, text=col)
            width = 80 if col == "Game" else 120
            self.history_tree.column(col, width=width, anchor=tk.CENTER)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_tree.pack(fill=tk.BOTH, expand=True)
        
        # Initial load of history
        self._refresh_history()
    
    def _register_player(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a player name")
            return
        
        try:
            result = self.server.register_player(name)
            self.reg_status.config(text=result)
            
            if "successfully" in result:
                self.player_name = name
                self.player_info_frame.pack(pady=10, fill=tk.X)
                self.player_info_label.config(text=f"Logged in as: {self.player_name}")
                self.name_entry.config(state=tk.DISABLED)
                self.register_button.config(state=tk.DISABLED)
                
                # Update status
                self.status_bar.config(text=f"Registered as {self.player_name}")
                
                # Go to play tab
                self.notebook.select(self.play_tab)
        except Exception as e:
            messagebox.showerror("Registration Error", str(e))
    
    def _play_game(self, choice):
        if not self.player_name:
            messagebox.showerror("Error", "Please register as a player first!")
            self.notebook.select(self.home_tab)
            return
        
        try:
            result = self.server.play(self.player_name, choice)
            
            # Update result text
            self.result_text.config(state=tk.NORMAL)
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.result_text.insert(tk.END, f"[{timestamp}] {result}\n\n")
            self.result_text.see(tk.END)  # Scroll to the bottom
            self.result_text.config(state=tk.DISABLED)
            
            # Update status
            self.status_bar.config(text=f"Game played: {choice}")
            
            # Refresh scores
            self._refresh_scores()
            self._refresh_history()
        except Exception as e:
            messagebox.showerror("Game Error", str(e))
    
    def _clear_results(self):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)
    
    def _refresh_scores(self):
        try:
            scores = self.server.get_all_scores()
            
            # Clear existing items
            for item in self.scores_tree.get_children():
                self.scores_tree.delete(item)
            
            # Add new items
            for player, score in scores.items():
                self.scores_tree.insert("", tk.END, values=(player, score))
            
            self.status_bar.config(text="Scores refreshed")
        except Exception as e:
            messagebox.showerror("Score Error", str(e))
    
    def _reset_scores(self):
        if messagebox.askyesno("Reset Scores", "Are you sure you want to reset all scores?"):
            try:
                result = self.server.reset_scores()
                messagebox.showinfo("Reset Scores", result)
                self._refresh_scores()
            except Exception as e:
                messagebox.showerror("Reset Error", str(e))
    
    def _refresh_history(self):
        try:
            history = self.server.get_game_history()
            
            # Clear existing items
            for item in self.history_tree.get_children():
                self.history_tree.delete(item)
            
            # Add new items
            for i, game in enumerate(history, 1):
                values = (
                    f"Game {i}",
                    game['player'], 
                    game['player_choice'], 
                    game['computer_choice'], 
                    game['result']
                )
                self.history_tree.insert("", tk.END, values=values)
            
            self.status_bar.config(text="History refreshed")
        except Exception as e:
            messagebox.showerror("History Error", str(e))
    
    def _clear_history(self):
        if messagebox.askyesno("Clear History", "Are you sure you want to clear the game history?"):
            try:
                result = self.server.reset_game_history()
                messagebox.showinfo("Clear History", result)
                self._refresh_history()
            except Exception as e:
                messagebox.showerror("Clear Error", str(e))
    
    def _update_status(self):
        # Check if server is still accessible and update player info
        try:
            if self.player_name:
                score = self.server.get_score(self.player_name)
                if "not registered" in score:
                    self.status_bar.config(text="Player session expired. Please restart application.")
        except:
            self.status_bar.config(text="Server connection lost!")
        
        # Schedule the next update
        self.root.after(5000, self._update_status)  # every 5 seconds

if __name__ == "__main__":
    root = tk.Tk()
    app = RPSClientGUI(root)
    root.mainloop()