import json
from pathlib import Path


STATE_FILE = Path("config/game_state.json")
RECENT_LIMIT = 5


def _default_state():
    return {"favorites": [], "recent": []}


def _clean_ids(values):
    if not isinstance(values, list):
        return []

    cleaned = []
    for value in values:
        game_id = str(value).strip()
        if game_id and game_id not in cleaned:
            cleaned.append(game_id)

    return cleaned


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

    return {
        "favorites": _clean_ids(state.get("favorites", [])),
        "recent": _clean_ids(state.get("recent", []))[:RECENT_LIMIT],
    }


def save_game_state(state):
    """Persist user game state in the config directory."""

    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

    clean_state = {
        "favorites": _clean_ids(state.get("favorites", [])),
        "recent": _clean_ids(state.get("recent", []))[:RECENT_LIMIT],
    }

    with STATE_FILE.open("w", encoding="utf-8") as file:
        json.dump(clean_state, file, indent=4)
        file.write("\n")
