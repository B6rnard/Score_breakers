"""
Flask server to display scores on a LAN.
Serves scores as an HTML page that can be accessed by other devices on the network.
"""

import json
from pathlib import Path
from flask import Flask, render_template_string
import socket

DATA_DIR = Path("Data")
SCORES_FILE = DATA_DIR / "Scores.json"

app = Flask(__name__)

# HTML template for displaying scores
SCORES_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Score Breakers - LAN Scoreboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background: linear-gradient(135deg, #000000 0%, #1a1a2e 100%);
            color: #00ff00;
            font-family: 'Courier New', monospace;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        h1 {
            text-align: center;
            font-size: 3em;
            margin-bottom: 40px;
            text-shadow: 0 0 10px #00ff00;
            color: #ffff00;
        }
        
        .games-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
        }
        
        .game-section {
            border: 3px solid #00ff00;
            border-radius: 10px;
            padding: 20px;
            background: rgba(0, 0, 0, 0.7);
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
        }
        
        .game-title {
            text-align: center;
            font-size: 1.8em;
            margin-bottom: 20px;
            color: #00ffff;
            text-shadow: 0 0 5px #00ffff;
        }
        
        .scoreboard {
            width: 100%;
        }
        
        .score-row {
            display: grid;
            grid-template-columns: 1fr 2fr 1fr;
            gap: 20px;
            padding: 10px;
            border-bottom: 1px solid #00ff00;
            align-items: center;
        }
        
        .score-row:last-child {
            border-bottom: none;
        }
        
        .score-row.header {
            font-weight: bold;
            color: #ffff00;
            background: rgba(0, 255, 0, 0.1);
            border-bottom: 2px solid #00ff00;
        }
        
        .rank {
            text-align: center;
            font-size: 1.2em;
            color: #ff00ff;
            font-weight: bold;
        }
        
        .player-name {
            padding-left: 10px;
            color: #00ffff;
        }
        
        .score-value {
            text-align: right;
            padding-right: 10px;
            font-size: 1.1em;
            color: #00ff00;
            font-weight: bold;
        }
        
        .empty-message {
            text-align: center;
            padding: 20px;
            color: #888888;
            font-size: 0.9em;
        }
        
        .refresh-info {
            text-align: center;
            margin-top: 40px;
            color: #888888;
            font-size: 0.8em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎮 SCORE BREAKERS 🎮</h1>
        <h2 style="text-align: center; color: #00ff00; margin-bottom: 30px; font-size: 1.2em;">LAN Scoreboard</h2>
        
        <div class="games-grid">
            {% for game_key, game_title in games_info %}
                <div class="game-section">
                    <div class="game-title">{{ game_title }}</div>
                    <div class="scoreboard">
                        <div class="score-row header">
                            <div class="rank">RANK</div>
                            <div class="player-name">PLAYER</div>
                            <div class="score-value">SCORE</div>
                        </div>
                        {% set game_scores = scores[game_key] %}
                        {% if game_scores %}
                            {% for score_entry in game_scores[:10] %}
                                <div class="score-row">
                                    <div class="rank">#{{ loop.index }}</div>
                                    <div class="player-name">{{ score_entry.player }}</div>
                                    <div class="score-value">{{ "{:,}".format(score_entry.score) }}</div>
                                </div>
                            {% endfor %}
                        {% else %}
                            <div class="empty-message">No scores yet.</div>
                        {% endif %}
                    </div>
                </div>
            {% endfor %}
        </div>
        
        <div class="refresh-info">
            <p>Page refreshes every 5 seconds</p>
            <p style="margin-top: 10px;">Access this from other devices at: <strong>http://{{ local_ip }}:5000</strong></p>
        </div>
    </div>
    
    <script>
        // Auto-refresh every 5 seconds
        setTimeout(function() {
            location.reload();
        }, 5000);
    </script>
</body>
</html>
"""


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
    local_ip = get_local_ip()
    
    games_info = [
        ("game1", "Game 1 - T-Rex Runner"),
        ("game2", "Game 2 - Orb Defender"),
        ("game3", "Game 3"),
    ]
    
    return render_template_string(
        SCORES_TEMPLATE,
        scores=scores,
        games_info=games_info,
        local_ip=local_ip
    )


def run_server(host="0.0.0.0", port=5000):
    """Run the Flask server."""
    print(f"Starting Flask server on {host}:{port}")
    print(f"Access scores at: http://{get_local_ip()}:{port}")
    app.run(host=host, port=port, debug=False, use_reloader=False)


if __name__ == "__main__":
    run_server()
