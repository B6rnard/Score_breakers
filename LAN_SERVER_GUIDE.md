# Score Breakers - LAN Server Guide

## New Feature: LAN Scoreboard Display

You now have a **LAN Server button** in the top-right corner of the application that allows you to host a live scoreboard on your local network.

### How to Use

1. **Start the Server**: Click the green **🖥️ Start LAN** button in the top-right corner of the application
2. **Access from Other Devices**: 
   - A status message will appear showing the URL (e.g., `http://192.168.1.100:5000`)
   - On any device connected to the same network, open a browser and go to that URL
   - You'll see a live, auto-refreshing scoreboard with all game scores

3. **Stop the Server**: Click the red **🖥️ Stop LAN** button to turn off the server

### Features

- **Beautiful Arcade Interface**: The web page has a retro arcade aesthetic with neon styling
- **Auto-Refresh**: The scoreboard automatically refreshes every 5 seconds
- **Multi-Game Support**: Displays scores for all games (Game 1, Game 2, Game 3)
- **Top 10 Rankings**: Shows the top 10 scores for each game
- **LAN Access**: Anyone on your local network can view the scores in real-time

### Technical Details

- **Port**: The server runs on port `5000` by default
- **Local IP**: The application detects your local IP address and displays it
- **Threading**: The Flask server runs in a background thread so it doesn't freeze the GUI
- **Persistent**: Scores are read from your `Data/Scores.json` file in real-time

### Network Access

To access the scoreboard from another device on your LAN:
1. Note the IP address shown in the status box (e.g., `192.168.1.100`)
2. Open a web browser on the other device
3. Visit `http://<your_ip>:5000`
4. The scoreboard will display and auto-refresh every 5 seconds

### Troubleshooting

- **Can't see the server from another device?**
  - Make sure both devices are on the same WiFi network
  - Check that your firewall isn't blocking port 5000
  - Try accessing `http://localhost:5000` from the same machine first

- **Server won't start?**
  - Make sure Flask is installed: `pip install Flask`
  - Check that port 5000 isn't already in use

- **No scores displaying?**
  - Make sure you've played and saved scores first
  - Check that `Data/Scores.json` file exists

### Files Added/Modified

- **flask_server.py** (NEW): Flask application that serves the scoreboard webpage
- **Main.py** (MODIFIED): Added the LAN button in the top-right corner
- **requirements.txt** (NEW): Lists Flask as a dependency

### Installation

If Flask is not installed, run:
```bash
pip install -r requirements.txt
```
