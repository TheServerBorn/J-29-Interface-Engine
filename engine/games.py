from engine.config import load_config


DEFAULT_LIBRARY_FOLDER = "PROGRAMS"
DEFAULT_LAUNCH_TYPE = "EXECUTABLE"


def _clean(value):
    return str(value or "").strip()


def _clean_upper(value):
    return _clean(value).upper()


def _parse_bool(value, default=False):
    text = _clean(value).lower()

    if text in {"1", "true", "yes", "on"}:
        return True

    if text in {"0", "false", "no", "off"}:
        return False

    return default


def _parse_year(value):
    text = _clean(value)

    if not text:
        return None

    try:
        return int(text)
    except ValueError:
        return None


def load_games(config_path="config/games.ini"):
    """Load the configured game library into structured metadata records.

    v0.21 keeps the legacy ``name``, ``path``, and ``folder`` keys intact so
    the existing terminal shell continues to work while adding richer fields
    that later integrations can consume.
    """

    config = load_config(config_path)
    games = []

    for section in config.sections():
        entry = config[section]

        name = _clean(entry.get("name", section)) or section

        # ``path`` remains the backwards-compatible executable path. New
        # launchers can use executable_path/rom_path based on launch_type.
        legacy_path = _clean(entry.get("path", ""))
        executable_path = _clean(entry.get("executable_path", legacy_path))
        rom_path = _clean(entry.get("rom_path", ""))

        folder = _clean(entry.get("folder", DEFAULT_LIBRARY_FOLDER))
        if not folder:
            folder = DEFAULT_LIBRARY_FOLDER

        platform = _clean_upper(entry.get("platform", folder))
        if not platform:
            platform = folder.upper()

        launch_type = _clean_upper(
            entry.get("launch_type", DEFAULT_LAUNCH_TYPE)
        )
        if not launch_type:
            launch_type = DEFAULT_LAUNCH_TYPE

        launch_path = executable_path
        if launch_type == "ROM" and rom_path:
            launch_path = rom_path

        games.append({
            "id": section,
            "name": name,
            "title": _clean(entry.get("title", name)) or name,
            "folder": folder.upper(),
            "platform": platform,
            "year": _parse_year(entry.get("year", "")),
            "genre": _clean(entry.get("genre", "")),
            "developer": _clean(entry.get("developer", "")),
            "publisher": _clean(entry.get("publisher", "")),
            "launch_type": launch_type,
            "path": launch_path,
            "executable_path": executable_path,
            "rom_path": rom_path,
            "emulator": _clean(entry.get("emulator", "")),
            "steam_id": _clean(entry.get("steam_id", "")),
            "favorite": _parse_bool(entry.get("favorite", "false")),
        })

    return games
