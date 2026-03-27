import tkinter as tk
import threading
import socket
from flask_server import run_server, get_local_ip

from Data.Scores import load_scores
from GUI.Menu import ArcadeMenu
from GUI.Profile import ProfileView


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
        self.server_thread = None
        self.server_running = False

        # Profile label and button (always visible - top left)
        self.profile_label = tk.Label(
            self.root,
            text=f"Profile: {self.current_profile}",
            font=("Arial", 12),
            fg="white",
            bg="black",
        )
        self.profile_label.place(x=10, y=10)

        self.profile_button = tk.Button(
            self.root,
            text="👤",
            font=("Arial", 10, "bold"),
            bg="darkblue",
            fg="white",
            command=self.open_profile_view,
            cursor="hand2",
        )
        self.profile_button.place(x=150, y=10, width=30, height=25)

        # LAN Server button frame (always visible - top right)
        self._setup_server_controls()

        # Helper to clear everything except the profile label/button and server controls
        def clear_main_area() -> None:
            for widget in self.root.winfo_children():
                # Only keep the profile label/button, server frame, and server status
                if (widget is not self.profile_label and 
                    widget is not self.profile_button and 
                    widget is not self.server_frame and 
                    widget is not self.server_status):
                    widget.destroy()

        self.clear_main_area = clear_main_area

        # Start on main menu
        self.menu = ArcadeMenu(
            self.root,
            self.scores,
            self.current_profile,
            clear_callback=self.clear_main_area,
        )

    def open_profile_view(self) -> None:
        """Open the profile selection view."""
        ProfileView(
            self.root,
            self.current_profile,
            on_profile_selected=self.change_profile,
            on_back=self.return_to_menu,
            clear_callback=self.clear_main_area,
        )

    def change_profile(self, new_profile: str) -> None:
        """Change the current profile."""
        self.current_profile = new_profile
        self.profile_label.config(text=f"Profile: {self.current_profile}")
        # Update the menu with new profile
        self.menu = ArcadeMenu(
            self.root,
            self.scores,
            self.current_profile,
            clear_callback=self.clear_main_area,
        )

    def return_to_menu(self) -> None:
        """Return to the main menu."""
        self.menu = ArcadeMenu(
            self.root,
            self.scores,
            self.current_profile,
            clear_callback=self.clear_main_area,
        )

    def _setup_server_controls(self) -> None:
        """Create the server control button and status indicator in the top right."""
        self.server_frame = tk.Frame(self.root, bg="black")
        self.server_frame.place(x=650, y=10, width=140, height=50)

        self.server_button = tk.Button(
            self.server_frame,
            text="🖥️ Start LAN",
            font=("Arial", 10, "bold"),
            bg="darkgreen",
            fg="white",
            command=self.toggle_lan_server,
            cursor="hand2",
        )
        self.server_button.pack(fill=tk.BOTH, expand=True)

        self.server_status = tk.Label(
            self.root,
            text="",
            font=("Arial", 8),
            fg="gray",
            bg="black",
        )
        self.server_status.place(x=600, y=60)

    def toggle_lan_server(self) -> None:
        """Start or stop the LAN server."""
        if self.server_running:
            self.stop_lan_server()
        else:
            self.start_lan_server()

    def start_lan_server(self) -> None:
        """Start the Flask LAN server in a background thread."""
        if self.server_running:
            return

        self.server_running = True
        self.server_button.config(text="🖥️ Stop LAN", bg="darkred")
        
        try:
            local_ip = get_local_ip()
            status_text = f"Running at\nhttp://{local_ip}:5000"
            self.server_status.config(text=status_text, fg="lime")
        except:
            self.server_status.config(text="Server starting...", fg="yellow")

        # Start Flask server in a background thread (daemon so it closes with app)
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()

    def stop_lan_server(self) -> None:
        """Stop the Flask server (note: Flask doesn't have a clean stop, so we just reset the flag)."""
        self.server_running = False
        self.server_button.config(text="🖥️ Start LAN", bg="darkgreen")
        self.server_status.config(text="", fg="gray")



if __name__ == "__main__":
    root = tk.Tk()
    app = ScoreBreakersApp(root)
    root.mainloop()
