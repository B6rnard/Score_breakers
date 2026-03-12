import tkinter as tk
from typing import Callable, Dict, Any


class TRexGame:
    """
    Very simple endless runner inspired by the T-Rex game.
    - Space/Up arrow to jump.
    - Avoid hitting the cactus.
    - Score increases over time.
    """

    def __init__(
        self,
        root: tk.Tk,
        on_exit: Callable[[], None],
        current_profile: str = "Guest",
        scores: Dict[str, Any] | None = None,
    ) -> None:
        self.root = root
        self.on_exit = on_exit
        self.current_profile = current_profile
        # scores is expected to be a ScoresDB instance, but we keep a fallback
        self.scores = scores

        # Game config
        self.canvas_width = 800
        self.canvas_height = 400
        self.ground_y = 320
        self.game_speed = 8
        self.jump_strength = -18
        self.gravity = 1.2

        # Game state
        self.is_running = False
        self.trex_y_vel = 0.0
        self.score = 0

        # UI setup
        self._build_view()
        self._bind_keys()

    def _build_view(self) -> None:
        """Create the canvas and basic labels/buttons."""
        self.frame = tk.Frame(self.root, bg="black")
        self.frame.pack(fill="both", expand=True)

        title = tk.Label(
            self.frame,
            text="Game 1 - T-Rex Runner",
            font=("Arial", 20, "bold"),
            fg="yellow",
            bg="black",
        )
        title.pack(pady=10)

        self.canvas = tk.Canvas(
            self.frame,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="black",
            highlightthickness=0,
        )
        self.canvas.pack(pady=10)

        # Ground line
        self.canvas.create_line(
            0, self.ground_y + 30, self.canvas_width, self.ground_y + 30, fill="white"
        )

        # T-Rex (simple rectangle)
        self.trex_width = 40
        self.trex_height = 50
        self.trex_x = 100
        self.trex_y = self.ground_y - self.trex_height

        self.trex = self.canvas.create_rectangle(
            self.trex_x,
            self.trex_y,
            self.trex_x + self.trex_width,
            self.trex_y + self.trex_height,
            fill="white",
        )

        # Cactus (simple rectangle)
        self.cactus_width = 30
        self.cactus_height = 60
        self.cactus_x = self.canvas_width + 100
        self.cactus_y = self.ground_y - self.cactus_height

        self.cactus = self.canvas.create_rectangle(
            self.cactus_x,
            self.cactus_y,
            self.cactus_x + self.cactus_width,
            self.cactus_y + self.cactus_height,
            fill="green",
        )

        # Score label
        self.score_label = tk.Label(
            self.frame,
            text="Score: 0",
            font=("Arial", 14),
            fg="white",
            bg="black",
        )
        self.score_label.pack()

        # Control buttons
        button_frame = tk.Frame(self.frame, bg="black")
        button_frame.pack(pady=10)

        self.start_button = tk.Button(
            button_frame,
            text="Start",
            font=("Arial", 14),
            command=self.start_game,
        )
        self.start_button.pack(side="left", padx=5)

        self.exit_button = tk.Button(
            button_frame,
            text="Exit to Menu",
            font=("Arial", 14),
            command=self.exit_to_menu,
        )
        self.exit_button.pack(side="left", padx=5)

        # Game over text handle
        self.game_over_text_id = None

    def _bind_keys(self) -> None:
        """Bind jump keys to the main window."""
        self.root.bind("<space>", self._on_jump)
        self.root.bind("<Up>", self._on_jump)

    def _unbind_keys(self) -> None:
        """Unbind keys when leaving the game."""
        self.root.unbind("<space>")
        self.root.unbind("<Up>")

    def _on_jump(self, event=None) -> None:
        """Handle jump input."""
        if not self.is_running:
            return
        # Only allow jump if on the ground
        current_y1, current_y2 = self._trex_bounds()[1], self._trex_bounds()[3]
        if current_y2 >= self.ground_y:
            self.trex_y_vel = self.jump_strength

    def _trex_bounds(self):
        return self.canvas.coords(self.trex)

    def _cactus_bounds(self):
        return self.canvas.coords(self.cactus)

    def start_game(self) -> None:
        """Reset and start the game loop."""
        self.is_running = True
        self.score = 0
        self.trex_y_vel = 0
        self.score_label.config(text="Score: 0")

        # Reset positions
        self.trex_y = self.ground_y - self.trex_height
        self.canvas.coords(
            self.trex,
            self.trex_x,
            self.trex_y,
            self.trex_x + self.trex_width,
            self.trex_y + self.trex_height,
        )

        self.cactus_x = self.canvas_width + 100
        self.canvas.coords(
            self.cactus,
            self.cactus_x,
            self.cactus_y,
            self.cactus_x + self.cactus_width,
            self.cactus_y + self.cactus_height,
        )

        # Remove old "Game Over" text if present
        if self.game_over_text_id is not None:
            self.canvas.delete(self.game_over_text_id)
            self.game_over_text_id = None

        self._game_loop()

    def _game_loop(self) -> None:
        """Main game loop using Tkinter's after."""
        if not self.is_running:
            return

        # Update T-Rex vertical movement
        self.trex_y_vel += self.gravity
        self.trex_y += self.trex_y_vel

        # Don't fall through ground
        if self.trex_y + self.trex_height >= self.ground_y:
            self.trex_y = self.ground_y - self.trex_height
            self.trex_y_vel = 0

        self.canvas.coords(
            self.trex,
            self.trex_x,
            self.trex_y,
            self.trex_x + self.trex_width,
            self.trex_y + self.trex_height,
        )

        # Move cactus to the left
        self.cactus_x -= self.game_speed
        if self.cactus_x + self.cactus_width < 0:
            # Respawn cactus offscreen to the right
            self.cactus_x = self.canvas_width + 50

        self.canvas.coords(
            self.cactus,
            self.cactus_x,
            self.cactus_y,
            self.cactus_x + self.cactus_width,
            self.cactus_y + self.cactus_height,
        )

        # Update score
        self.score += 1
        self.score_label.config(text=f"Score: {self.score}")

        # Check collision
        if self._check_collision():
            self._game_over()
            return

        # Schedule next frame
        self.root.after(30, self._game_loop)

    def _check_collision(self) -> bool:
        """Axis-Aligned Bounding Box (AABB) collision detection."""
        t_x1, t_y1, t_x2, t_y2 = self._trex_bounds()
        c_x1, c_y1, c_x2, c_y2 = self._cactus_bounds()

        overlap_x = t_x1 < c_x2 and t_x2 > c_x1
        overlap_y = t_y1 < c_y2 and t_y2 > c_y1
        return overlap_x and overlap_y
    def _game_over(self) -> None:
        """Stop the game and show 'Game Over' and store the score."""
        self.is_running = False

        # Save score via ScoresDB if available
        if self.scores is not None:
            try:
                # "game1" key is used by the scoreboard
                self.scores.add_score("game1", self.current_profile, self.score)
                self.scores.save()
            except AttributeError:
                # If scores is not a ScoresDB, just ignore (template fallback)
                pass

        self.game_over_text_id = self.canvas.create_text(
            self.canvas_width // 2,
            self.canvas_height // 2,
            text=f"GAME OVER\nScore: {self.score}",
            fill="red",
            font=("Arial", 24, "bold"),
        )
        # to save the score for current_profile under "game1".

    def exit_to_menu(self) -> None:
        """Clean up and go back to menu."""
        self.is_running = False
        self._unbind_keys()
        self.frame.destroy()
        self.on_exit()
        self.scores.add_score("game2", self.current_profile, final_score)
        self.scores.save()
