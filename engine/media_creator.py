"""J-29 physical-media authoring helpers.

v0.29 begins by generating the same j29-media.ini format that the v0.27
reader already understands.  This module deliberately has no UI and performs
no filesystem writes in the first checkpoint; the shell can preview a fully
validated descriptor before target-media selection is introduced.
"""

from configparser import ConfigParser
from io import StringIO


MEDIA_SECTION = "J29_MEDIA"
SUPPORTED_TARGET_LAUNCH_TYPES = {"EXECUTABLE", "ROM", "STEAM"}


class MediaCreatorError(ValueError):
    """Raised when a library record cannot safely become J-29 media."""


def _clean(value):
    return str(value or "").strip()


def is_launch_key_eligible(game):
    """Return True when a normal library game is safe to target by stable ID."""
    if not game:
        return False

    game_id = _clean(game.get("id"))
    launch_type = _clean(game.get("launch_type")).upper()
    source = _clean(game.get("source")).upper()

    if not game_id:
        return False

    # Do not author launch keys that point at another launch key or at media
    # that must itself remain inserted.  The creator should target the normal
    # installed/discovered library record instead.
    if launch_type == "LIBRARY" or source == "PHYSICAL_MEDIA":
        return False

    return launch_type in SUPPORTED_TARGET_LAUNCH_TYPES


def eligible_launch_key_games(games):
    """Return creator-safe games in a predictable user-facing order."""
    eligible = [game for game in (games or []) if is_launch_key_eligible(game)]
    return sorted(
        eligible,
        key=lambda game: (
            _clean(game.get("platform") or game.get("folder")).casefold(),
            _clean(game.get("title") or game.get("name")).casefold(),
            _clean(game.get("id")).casefold(),
        ),
    )


def _launch_key_fields(game):
    if not is_launch_key_eligible(game):
        raise MediaCreatorError("PROGRAM CANNOT BE USED AS A MEDIA LAUNCH KEY")

    game_id = _clean(game.get("id"))
    title = _clean(game.get("title") or game.get("name") or game_id)
    platform = _clean(game.get("platform") or game.get("folder") or "MEDIA").upper()

    return {
        "type": "GAME",
        "title": title,
        "platform": platform,
        "game_id": game_id,
    }


def build_launch_key_descriptor(game):
    """Build a complete j29-media.ini launch-key descriptor as UTF-8 text."""
    fields = _launch_key_fields(game)

    parser = ConfigParser()
    parser.optionxform = str.lower
    parser[MEDIA_SECTION] = fields

    buffer = StringIO()
    parser.write(buffer, space_around_delimiters=False)
    return buffer.getvalue().strip() + "\n"


def validate_launch_key_descriptor(text):
    """Validate creator output without relying on a mounted target volume."""
    parser = ConfigParser()
    try:
        parser.read_string(str(text or ""))
    except Exception as exc:
        return False, f"INVALID MEDIA METADATA: {exc}"

    if not parser.has_section(MEDIA_SECTION):
        return False, "J29_MEDIA SECTION NOT FOUND"

    section = parser[MEDIA_SECTION]
    if section.get("type", "").strip().upper() != "GAME":
        return False, "MEDIA TYPE MUST BE GAME"
    if not section.get("title", "").strip():
        return False, "MEDIA TITLE NOT PROVIDED"
    if not section.get("game_id", "").strip():
        return False, "LIBRARY GAME ID NOT PROVIDED"

    return True, "READY"


def preview_launch_key(game):
    """Return user-facing preview data plus the hidden descriptor text."""
    fields = _launch_key_fields(game)
    descriptor = build_launch_key_descriptor(game)
    valid, status = validate_launch_key_descriptor(descriptor)

    if not valid:
        raise MediaCreatorError(status)

    return {
        "media_type": "GAME LAUNCH KEY",
        "title": fields["title"],
        "platform": fields["platform"],
        "target": "LIBRARY PROGRAM",
        "status": status,
        "descriptor": descriptor,
    }
