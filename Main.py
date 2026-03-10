import tkinter as tk
import json
import os

# Main application class for Score Breakers
class ScoreBreakersApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Score Breakers - Arcade Games")
        self.root.geometry("800x600")
        self.root.configure(bg="black")

        # Load profiles and scores
        self.profiles = self.load_profiles()
        self.scores = self.load_scores()
        self.current_profile = "Guest"  # Default profile

        # Profile label in top left corner
        self.profile_label = tk.Label(self.root, text=f"Profile: {self.current_profile}", font=("Arial", 12), fg="white", bg="black")
        self.profile_label.place(x=10, y=10)

        # Game selection screen
        self.show_game_selection()

    def load_profiles(self):
        # Load profiles from Data/Profiles.json
        try:
            with open("Data/Profiles.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}

    def load_scores(self):
        # Load scores from Data/Scores.py (assuming it's a dict or something)
        # For now, placeholder
        return {"game1": [], "game2": []}

    def show_game_selection(self):
        # Clear current widgets if any
        for widget in self.root.winfo_children():
            if widget != self.profile_label:
                widget.destroy()

        # Title for game selection
        self.title_label = tk.Label(self.root, text="Select a Game", font=("Arial", 24, "bold"), fg="yellow", bg="black")
        self.title_label.pack(pady=50)

        # Frame for game buttons
        self.game_frame = tk.Frame(self.root, bg="black")
        self.game_frame.pack()

        # Game buttons with scoreboard access
        self.game1_button = tk.Button(self.game_frame, text="Game 1 - View Scoreboard", font=("Arial", 16), command=lambda: self.show_scoreboard(1))
        self.game1_button.pack(pady=10)

        self.game2_button = tk.Button(self.game_frame, text="Game 2 - View Scoreboard", font=("Arial", 16), command=lambda: self.show_scoreboard(2))
        self.game2_button.pack(pady=10)

    def show_scoreboard(self, game_num):
        # Clear screen
        for widget in self.root.winfo_children():
            if widget != self.profile_label:
                widget.destroy()

        # Scoreboard title
        self.scoreboard_label = tk.Label(self.root, text=f"Scoreboard for Game {game_num}", font=("Arial", 20, "bold"), fg="yellow", bg="black")
        self.scoreboard_label.pack(pady=20)

        # Display scores (placeholder)
        scores = self.scores.get(f"game{game_num}", [])
        if scores:
            for score in scores:
                score_label = tk.Label(self.root, text=f"{score['player']}: {score['score']}", font=("Arial", 14), fg="white", bg="black")
                score_label.pack()
        else:
            no_scores_label = tk.Label(self.root, text="No scores yet", font=("Arial", 14), fg="white", bg="black")
            no_scores_label.pack()

        # Back button
        back_button = tk.Button(self.root, text="Back to Game Selection", font=("Arial", 16), command=self.show_game_selection)
        back_button.pack(pady=20)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ScoreBreakersApp(root)
    root.mainloop()
