import json
from pathlib import Path


STATE_FILE = Path("config/game_state.json")


def load_game_state():
    if not STATE_FILE.exists():
        return {
            "favorites": [],
            "recent": []
        }

    with open(STATE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_game_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as file:
        json.dump(state, file, indent=4)