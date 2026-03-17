import tkinter as tk
from typing import Dict, Any

from GUI.Scoreboard import ScoreboardView
from Games.Game_1 import TRexGame
from Games.Game_2 import OrbDefender


class ArcadeMenu:
    """
    Main game selection screen.
    Uses templates (Tkinter widgets) and calls ScoreboardView when needed.
    """

    def __init__(
        self,
        root: tk.Tk,
        scores: Dict[str, Any],
        current_profile: str,
        clear_callback,
    ) -> None:
        self.root = root
        self.scores = scores
        self.current_profile = current_profile
        # Function provided by Main to clear everything except profile label
        self.clear_callback = clear_callback

        self._build_menu()

    def _clear_screen(self) -> None:
        """Use the shared clear function from Main."""
        self.clear_callback()

    def _build_menu(self) -> None:
        """Template: main arcade menu view."""
        self._clear_screen()

        title_label = tk.Label(
            self.root,
            text="Select a Game",
            font=("Arial", 24, "bold"),
            fg="yellow",
            bg="black",
        )
        title_label.pack(pady=50)

        game_frame = tk.Frame(self.root, bg="black")
        game_frame.pack()

        # Game 1 controls
        game1_title = tk.Label(
            game_frame,
            text="Game 1 - T-Rex Runner",
            font=("Arial", 18, "bold"),
            fg="cyan",
            bg="black",
        )
        game1_title.pack(pady=(0, 5))

        game1_play_button = tk.Button(
            game_frame,
            text="Play Game 1",
            font=("Arial", 16),
            command=self.play_game1,
        )
        game1_play_button.pack(pady=5)

        game1_score_button = tk.Button(
            game_frame,
            text="Game 1 - View Scoreboard",
            font=("Arial", 14),
            command=lambda: self.open_scoreboard(1),
        )
        game1_score_button.pack(pady=(0, 15))

        # Game 2 controls
        game2_title = tk.Label(
            game_frame,
            text="Game 2 - Orb Defender",
            font=("Arial", 18, "bold"),
            fg="cyan",
            bg="black",
        )
        game2_title.pack(pady=(0, 5))

        game2_play_button = tk.Button(
            game_frame,
            text="Play Game 2",
            font=("Arial", 16),
            command=self.play_game2,
        )
        game2_play_button.pack(pady=5)

        game2_score_button = tk.Button(
            game_frame,
            text="Game 2 - View Scoreboard",
            font=("Arial", 14),
            command=lambda: self.open_scoreboard(2),
        )
        game2_score_button.pack(pady=(0, 15))

    def play_game1(self) -> None:
        """Start Game 1 (T-Rex runner) inside the main window."""
        self._clear_screen()

        # When the game exits, rebuild the menu
        TRexGame(
            self.root,
            on_exit=self._build_menu,
            current_profile=self.current_profile,
            scores=self.scores,
        )

    def play_game2(self) -> None:
        """Start Game 2 (Orb Defender) inside the main window."""
        self._clear_screen()

        # When the game exits, rebuild the menu
        OrbDefender(
            self.root,
            on_exit=self._build_menu,
            current_profile=self.current_profile,
            scores=self.scores,
        )

    def open_scoreboard(self, game_num: int) -> None:
        """Switch to scoreboard view for a given game."""
        ScoreboardView(
            self.root,
            self.scores,
            game_num,
            on_back=self._build_menu,
            clear_callback=self.clear_callback,
        )