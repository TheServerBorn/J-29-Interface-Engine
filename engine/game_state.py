import json
from pathlib import Path


STATE_FILE = Path("config/game_state.json")


def _default_state():
    return {"favorites": []}


def load_game_state():
    """Load persistent user game state without making startup fragile."""

    if not STATE_FILE.exists():
        return _default_state()

    try:
        with STATE_FILE.open("r", encoding="utf-8") as file:
            state = json.load(file)
    except (OSError, json.JSONDecodeError):
        return _default_state()

    if not isinstance(state, dict):
        return _default_state()

    favorites = state.get("favorites", [])
    if not isinstance(favorites, list):
        favorites = []

    return {
        "favorites": [
            str(game_id)
            for game_id in favorites
            if str(game_id).strip()
        ]
    }


def save_game_state(state):
    """Persist user game state in the config directory."""

    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

    clean_state = {
        "favorites": list(dict.fromkeys(state.get("favorites", [])))
    }

    with STATE_FILE.open("w", encoding="utf-8") as file:
        json.dump(clean_state, file, indent=4)
        file.write("\n")
