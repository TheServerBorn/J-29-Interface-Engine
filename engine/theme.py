from engine.config import load_config


def load_theme(theme_path="themes/callisto_green/theme.ini"):
    config = load_config(theme_path)

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
    }