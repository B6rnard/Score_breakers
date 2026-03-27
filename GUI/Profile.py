import tkinter as tk
from typing import Dict, Any, Callable, List
import json
from pathlib import Path

DATA_DIR = Path("Data")
PROFILES_FILE = DATA_DIR / "Profiles.json"


def load_profiles() -> List[str]:
    """Load list of profile names from JSON file."""
    if not PROFILES_FILE.exists():
        return ["Guest"]
    
    try:
        with PROFILES_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
            profiles = data.get("profiles", [])
            return profiles if profiles else ["Guest"]
    except (json.JSONDecodeError, OSError):
        return ["Guest"]


def save_profiles(profiles: List[str]) -> None:
    """Save list of profile names to JSON file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with PROFILES_FILE.open("w", encoding="utf-8") as f:
        json.dump({"profiles": profiles}, f, indent=2)


class ProfileView:
    """
    Profile selection and management screen.
    Allows selecting existing profiles or creating new ones.
    """

    def __init__(
        self,
        root: tk.Tk,
        current_profile: str,
        on_profile_selected: Callable[[str], None],
        on_back: Callable[[], None],
        clear_callback,
    ) -> None:
        self.root = root
        self.current_profile = current_profile
        self.on_profile_selected = on_profile_selected
        self.on_back = on_back
        # Function provided by Main to clear everything except profile label
        self.clear_callback = clear_callback

        self._build_profile_view()

    def _clear_screen(self) -> None:
        """Use the shared clear function from Main."""
        self.clear_callback()

    def _build_profile_view(self) -> None:
        """Template: profile selection view."""
        self._clear_screen()

        title = tk.Label(
            self.root,
            text="Select Profile",
            font=("Arial", 24, "bold"),
            fg="yellow",
            bg="black",
        )
        title.pack(pady=30)

        # Load existing profiles
        self.profiles = load_profiles()

        # Profile list frame
        list_frame = tk.Frame(self.root, bg="black")
        list_frame.pack(pady=20)

        # Current profile indicator
        current_label = tk.Label(
            list_frame,
            text=f"Current: {self.current_profile}",
            font=("Arial", 14, "bold"),
            fg="lime",
            bg="black",
        )
        current_label.pack(pady=(0, 20))

        # Profile buttons
        for profile in self.profiles:
            btn = tk.Button(
                list_frame,
                text=profile,
                font=("Arial", 16),
                width=20,
                command=lambda p=profile: self.select_profile(p),
            )
            if profile == self.current_profile:
                btn.config(bg="darkblue", fg="white")
            btn.pack(pady=5)

        # New profile section
        new_frame = tk.Frame(self.root, bg="black")
        new_frame.pack(pady=20)

        new_label = tk.Label(
            new_frame,
            text="Create New Profile:",
            font=("Arial", 16, "bold"),
            fg="cyan",
            bg="black",
        )
        new_label.pack(pady=(0, 10))

        self.new_profile_entry = tk.Entry(
            new_frame,
            font=("Arial", 14),
            width=25,
        )
        self.new_profile_entry.pack(pady=5)

        create_btn = tk.Button(
            new_frame,
            text="Create Profile",
            font=("Arial", 14),
            command=self.create_new_profile,
        )
        create_btn.pack(pady=10)

        # Back button
        back_btn = tk.Button(
            self.root,
            text="Back to Menu",
            font=("Arial", 16),
            command=self.on_back,
        )
        back_btn.pack(pady=30)

    def select_profile(self, profile: str) -> None:
        """Select a profile and return to menu."""
        self.on_profile_selected(profile)
        self.on_back()

    def create_new_profile(self) -> None:
        """Create a new profile if name is valid."""
        new_name = self.new_profile_entry.get().strip()
        
        if not new_name:
            return
        
        if new_name in self.profiles:
            # Profile already exists, just select it
            self.select_profile(new_name)
            return
        
        # Add new profile
        self.profiles.append(new_name)
        save_profiles(self.profiles)
        
        # Select the new profile
        self.select_profile(new_name)
