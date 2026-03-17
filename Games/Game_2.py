import tkinter as tk
import random
from typing import Callable, Dict, Any


class OrbDefender:
    """
    Original arcade game: Orb Defender.
    - Control a defender at the bottom with left/right arrows.
    - Press space to shoot lasers at falling orbs.
    - Orbs are worth points based on color: red=10, blue=20, green=30.
    - If an orb hits the bottom, game over.
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
        self.scores = scores

        # Game config
        self.canvas_width = 800
        self.canvas_height = 400
        self.defender_speed = 10
        self.laser_speed = -15  # upwards
        self.orb_speed = 3
        self.orb_spawn_rate = 50  # frames

        # Game state
        self.is_running = False
        self.score = 0
        self.frame_count = 0
        self.defender_x = self.canvas_width // 2
        self.lasers = []  # list of (x, y) tuples
        self.orbs = []  # list of (x, y, color, points) tuples

        # UI setup
        self._build_view()
        self._bind_keys()

    def _build_view(self) -> None:
        """Create the canvas and basic labels/buttons."""
        self.frame = tk.Frame(self.root, bg="black")
        self.frame.pack(fill="both", expand=True)

        title = tk.Label(
            self.frame,
            text="Game 2 - Orb Defender",
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

        # Defender (paddle at bottom)
        self.defender_width = 60
        self.defender_height = 20
        self.defender_y = self.canvas_height - self.defender_height - 10
        self.defender = self.canvas.create_rectangle(
            self.defender_x - self.defender_width // 2,
            self.defender_y,
            self.defender_x + self.defender_width // 2,
            self.defender_y + self.defender_height,
            fill="cyan",
        )

        # Score label
        self.score_label = tk.Label(
            self.frame,
            text=f"Score: {self.score}",
            font=("Arial", 16),
            fg="white",
            bg="black",
        )
        self.score_label.pack()

        # Start button
        self.start_button = tk.Button(
            self.frame,
            text="Start Game",
            font=("Arial", 16),
            command=self.start_game,
        )
        self.start_button.pack(pady=10)

        # Exit button
        self.exit_button = tk.Button(
            self.frame,
            text="Exit to Menu",
            font=("Arial", 16),
            command=self.exit_game,
        )
        self.exit_button.pack(pady=5)

    def _bind_keys(self) -> None:
        """Bind keys for movement and shooting."""
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<space>", self.shoot_laser)
        self.root.focus_set()

    def move_left(self, event) -> None:
        if self.is_running and self.defender_x > self.defender_width // 2:
            self.defender_x -= self.defender_speed
            self.canvas.coords(
                self.defender,
                self.defender_x - self.defender_width // 2,
                self.defender_y,
                self.defender_x + self.defender_width // 2,
                self.defender_y + self.defender_height,
            )

    def move_right(self, event) -> None:
        if self.is_running and self.defender_x < self.canvas_width - self.defender_width // 2:
            self.defender_x += self.defender_speed
            self.canvas.coords(
                self.defender,
                self.defender_x - self.defender_width // 2,
                self.defender_y,
                self.defender_x + self.defender_width // 2,
                self.defender_y + self.defender_height,
            )

    def shoot_laser(self, event) -> None:
        if self.is_running:
            laser_x = self.defender_x
            laser_y = self.defender_y
            laser = self.canvas.create_rectangle(
                laser_x - 2, laser_y, laser_x + 2, laser_y - 10, fill="yellow"
            )
            self.lasers.append((laser_x, laser_y, laser))

    def start_game(self) -> None:
        """Start the game loop."""
        self.is_running = True
        self.start_button.config(state="disabled")
        self.game_loop()

    def game_loop(self) -> None:
        if not self.is_running:
            return

        self.frame_count += 1

        # Spawn orbs
        if self.frame_count % self.orb_spawn_rate == 0:
            orb_x = random.randint(20, self.canvas_width - 20)
            orb_y = 0
            colors = [("red", 10), ("blue", 20), ("green", 30)]
            color, points = random.choice(colors)
            orb = self.canvas.create_oval(
                orb_x - 10, orb_y - 10, orb_x + 10, orb_y + 10, fill=color
            )
            self.orbs.append((orb_x, orb_y, orb, points))

        # Move orbs
        to_remove_orbs = []
        for i, (x, y, orb, points) in enumerate(self.orbs):
            y += self.orb_speed
            if y > self.canvas_height:
                # Game over
                self.game_over()
                return
            self.canvas.coords(orb, x - 10, y - 10, x + 10, y + 10)
            self.orbs[i] = (x, y, orb, points)

        # Move lasers
        to_remove_lasers = []
        for i, (x, y, laser) in enumerate(self.lasers):
            y += self.laser_speed
            if y < 0:
                self.canvas.delete(laser)
                to_remove_lasers.append(i)
            else:
                self.canvas.coords(laser, x - 2, y, x + 2, y - 10)
                self.lasers[i] = (x, y, laser)

        # Check collisions
        for li, (lx, ly, laser) in enumerate(self.lasers):
            for oi, (ox, oy, orb, points) in enumerate(self.orbs):
                if abs(lx - ox) < 15 and abs(ly - oy) < 15:
                    # Hit
                    self.score += points
                    self.score_label.config(text=f"Score: {self.score}")
                    self.canvas.delete(laser)
                    self.canvas.delete(orb)
                    to_remove_lasers.append(li)
                    to_remove_orbs.append(oi)
                    break

        # Remove collided items
        for i in sorted(to_remove_lasers, reverse=True):
            if i < len(self.lasers):
                del self.lasers[i]
        for i in sorted(to_remove_orbs, reverse=True):
            if i < len(self.orbs):
                del self.orbs[i]

        # Continue loop
        self.root.after(50, self.game_loop)

    def game_over(self) -> None:
        """End the game and save score."""
        self.is_running = False
        self.start_button.config(state="normal")

        # Save score
        if self.scores:
            try:
                self.scores.add_score("game2", self.current_profile, self.score)
                self.scores.save()
            except AttributeError:
                pass  # If scores is dict, skip

        # Show game over
        self.canvas.create_text(
            self.canvas_width // 2,
            self.canvas_height // 2,
            text=f"Game Over! Score: {self.score}",
            font=("Arial", 24, "bold"),
            fill="white",
        )

    def exit_game(self) -> None:
        """Exit to menu."""
        self.is_running = False
        self.frame.destroy()
        self.on_exit()
