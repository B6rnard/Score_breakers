import tkinter as tk
from typing import Dict, Any, Callable


class ScoreboardView:
    """
    Scoreboard screen for a single game.
    Displays scores and offers a back button.
    """

    def __init__(
        self,
        root: tk.Tk,
        scores: Dict[str, Any],
        game_num: int,
        on_back: Callable[[], None],
        clear_callback,
    ) -> None:
        self.root = root
        self.scores = scores
        self.game_num = game_num
        self.on_back = on_back
        # Function provided by Main to clear everything except profile label
        self.clear_callback = clear_callback

        self._build_scoreboard()

    def _clear_screen(self) -> None:
        """Use the shared clear function from Main."""
        self.clear_callback()

    def _build_scoreboard(self) -> None:
        """Template: scoreboard view."""
        self._clear_screen()

        title = tk.Label(
            self.root,
            text=f"Scoreboard for Game {self.game_num}",
            font=("Arial", 20, "bold"),
            fg="yellow",
            bg="black",
        )
        title.pack(pady=20)

        game_key = f"game{self.game_num}"
        # self.scores is a ScoresDB-like object
        try:
            scores_for_game = self.scores.get_game_scores(game_key)
        except AttributeError:
            # Backwards compatibility if a plain dict is ever passed
            scores_for_game = self.scores.get(game_key, [])

        if scores_for_game:
            for score in scores_for_game:
                text = f"{score.get('player', 'Unknown')}: {score.get('score', 0)}"
                score_label = tk.Label(
                    self.root,
                    text=text,
                    font=("Arial", 14),
                    fg="white",
                    bg="black",
                )
                score_label.pack()
        else:
            no_scores_label = tk.Label(
                self.root,
                text="No scores yet",
                font=("Arial", 14),
                fg="white",
                bg="black",
            )
            no_scores_label.pack()

        back_button = tk.Button(
            self.root,
            text="Back to Game Selection",
            font=("Arial", 16),
            command=self.on_back,
        )
        back_button.pack(pady=20)