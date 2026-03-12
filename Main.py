import tkinter as tk

from Data.Scores import load_scores
from GUI.Menu import ArcadeMenu


class ScoreBreakersApp:
    """
    Main application class.
    Keeps high-level state and delegates UI to GUI layer.
    """

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Score Breakers - Arcade Games")
        self.root.geometry("800x600")
        self.root.configure(bg="black")

        # Data layer
        # self.scores is a ScoresDB instance
        self.scores = load_scores()
        self.current_profile = "Guest"

        # Profile label (always visible)
        self.profile_label = tk.Label(
            self.root,
            text=f"Profile: {self.current_profile}",
            font=("Arial", 12),
            fg="white",
            bg="black",
        )
        self.profile_label.place(x=10, y=10)

        # Helper to clear everything except the profile label
        def clear_main_area() -> None:
            for widget in self.root.winfo_children():
                # Only keep the profile label
                if widget is not self.profile_label:
                    widget.destroy()

        self.clear_main_area = clear_main_area

        # Start on main menu
        self.menu = ArcadeMenu(
            self.root,
            self.scores,
            self.current_profile,
            clear_callback=self.clear_main_area,
        )

    # Later we can add methods like:
    # - change_profile()
    # - refresh_scores()


if __name__ == "__main__":
    root = tk.Tk()
    app = ScoreBreakersApp(root)
    root.mainloop()
