from pathlib import Path

from engine.config import load_config


def load_theme(theme_path="themes/callisto_green/theme.ini"):
    theme_file = Path(theme_path)
    config = load_config(theme_file)

    return {
        "name": config.get(
            "THEME",
            "name",
            fallback="Callisto Green"
        ),
        "background": config.get(
            "COLORS",
            "background",
            fallback="#000000"
        ),
        "primary": config.get(
            "COLORS",
            "primary",
            fallback="#39FF14"
        ),
        "secondary": config.get(
            "COLORS",
            "secondary",
            fallback="#167A10"
        ),
        "font_family": config.get(
            "FONT",
            "family",
            fallback="Courier New"
        ),
        "title_size": config.getint(
            "FONT",
            "title_size",
            fallback=24
        ),
        "menu_size": config.getint(
            "FONT",
            "menu_size",
            fallback=20
        ),
        "status_size": config.getint(
            "FONT",
            "status_size",
            fallback=14
        ),
        "cursor_size": config.getint(
            "FONT",
            "cursor_size",
            fallback=20
        ),
        "scanlines": config.getboolean(
            "CRT",
            "scanlines",
            fallback=True
        ),
        "scanline_spacing": config.getint(
            "CRT",
            "scanline_spacing",
            fallback=6
        ),
        "scanline_intensity": config.getint(
            "CRT",
            "scanline_intensity",
            fallback=40
        ),
        "cursor_style": config.get(
            "CURSOR",
            "style",
            fallback="BLOCK"
        ),
        # Keep audio presentation inside the theme. Each entry is resolved
        # relative to the selected theme directory by AudioManager.
        "sounds": {
            "boot": config.get("AUDIO", "boot", fallback="sounds/boot.wav"),
            "menu_move": config.get("AUDIO", "menu_move", fallback="sounds/menu_move.wav"),
            "select": config.get("AUDIO", "select", fallback="sounds/select.wav"),
            "error": config.get("AUDIO", "error", fallback="sounds/error.wav"),
            "media_detected": config.get("AUDIO", "media_detected", fallback="sounds/media_detected.wav"),
            "access_granted": config.get("AUDIO", "access_granted", fallback="sounds/access_granted.wav"),
            "access_denied": config.get("AUDIO", "access_denied", fallback="sounds/access_denied.wav"),
            "launch": config.get("AUDIO", "launch", fallback="sounds/launch.wav"),
            "shutdown": config.get("AUDIO", "shutdown", fallback="sounds/shutdown.wav"),
        },
        "_theme_dir": str(theme_file.parent),
    }
