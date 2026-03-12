"""
Data layer for scores.
Holds basic templates and simple loading/saving logic.
"""

import json
from pathlib import Path
from typing import Dict, Any, List

DATA_DIR = Path("Data")
SCORES_FILE = DATA_DIR / "Scores.json"


def default_scores() -> dict:
    """Template for initial scores."""
    return {
        "game1": [],
        "game2": [],
        "game3": [],
    }


class ScoresDB:
    """
    Simple score 'database' used by all games and the scoreboard.

    - Stores scores in-memory as a dict, e.g.:
      {
          "game1": [{"player": "Guest", "score": 123}],
          "game2": [],
          ...
      }
    - Persists to JSON on disk.
    """

    def __init__(self, data: Dict[str, Any] | None = None) -> None:
        self._data: Dict[str, Any] = data if data is not None else default_scores()
        # Ensure required keys always exist
        base = default_scores()
        for key in base:
            self._data.setdefault(key, [])

    # ---------- basic access ----------

    def get_raw(self) -> Dict[str, Any]:
        """Return the underlying dict (for passing to views)."""
        return self._data

    def get_game_scores(self, game_key: str) -> List[Dict[str, Any]]:
        """Return list of scores for a game, always a list."""
        return list(self._data.get(game_key, []))

    # ---------- update helpers ----------

    def add_score(self, game_key: str, player: str, score: int) -> None:
        """
        Add a score entry for a game.

        - game_key: e.g. "game1", "game2"
        - player: profile name
        - score: numeric score
        """
        if game_key not in self._data:
            self._data[game_key] = []

        self._data[game_key].append({"player": player, "score": int(score)})

        # Sort descending by score (highest first)
        self._data[game_key].sort(key=lambda s: s.get("score", 0), reverse=True)

    # ---------- persistence ----------

    def save(self) -> None:
        """Persist scores to the JSON file."""
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with SCORES_FILE.open("w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2)


def load_scores() -> ScoresDB:
    """Load scores into a ScoresDB instance, or return defaults."""
    if not SCORES_FILE.exists():
        return ScoresDB(default_scores())

    try:
        with SCORES_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return ScoresDB(default_scores())

    # Only keep keys we know about
    base = default_scores()
    cleaned: Dict[str, Any] = {k: data.get(k, []) for k in base.keys()}
    return ScoresDB(cleaned)