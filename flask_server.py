"""
Flask server to display scores on a LAN.
Serves scores as an HTML page that can be accessed by other devices on the network.
"""

import json
from pathlib import Path
from flask import Flask, render_template
import socket

DATA_DIR = Path("Data")
SCORES_FILE = DATA_DIR / "Scores.json"

app = Flask(__name__)


def load_scores_data():
    """Load scores from JSON file."""
    if not SCORES_FILE.exists():
        return {
            "game1": [],
            "game2": [],
            "game3": [],
        }
    
    try:
        with SCORES_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {
            "game1": [],
            "game2": [],
            "game3": [],
        }


def get_local_ip():
    """Get the local IP address of the machine."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"


@app.route("/")
def index():
    """Main scores display page."""
    scores = load_scores_data()
    # load data score from client
    local_ip = get_local_ip()
    
    games_info = [
        ("game1", "Game 1 - T-Rex Runner"),
        ("game2", "Game 2 - Orb Defender"),
        ("game3", "Game 3"),
    ]
    
    return render_template(
        "scoreboard.html",
        scores=scores,
        games_info=games_info,
        local_ip=local_ip
    )

# router to exchange scores with client (if needed in future)

# way to exchange ip address with client (if needed in future)
def run_server(host="0.0.0.0", port=5000):
    """Run the Flask server."""
    print(f"Starting Flask server on {host}:{port}")
    print(f"Access scores at: http://{get_local_ip()}:{port}")
    app.run(host=host, port=port, debug=False, use_reloader=False)


if __name__ == "__main__":
    run_server()
