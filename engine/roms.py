"""Automatic ROM library discovery for J-29.

ROM-specific filesystem knowledge stays in the engine. Shells receive the same
normal game records used by manually configured titles and Steam discovery.
"""

from __future__ import annotations

import configparser
import hashlib
import os
import re
import shutil
from pathlib import Path


_CONFIG_PATH = Path("config/roms.ini")
_EXAMPLE_PATH = Path("config/roms.example.ini")

# Canonical platform names used by J-29. Folder aliases are intentionally
# forgiving so existing collections do not need to be renamed.
_PLATFORM_ALIASES = {
    "snes": "SNES",
    "super nintendo": "SNES",
    "super nintendo entertainment system": "SNES",
    "nes": "NES",
    "nintendo entertainment system": "NES",
    "gb": "GB",
    "game boy": "GB",
    "gbc": "GBC",
    "game boy color": "GBC",
    "gba": "GBA",
    "game boy advance": "GBA",
    "ds": "DS",
    "nds": "DS",
    "nintendo ds": "DS",
    "genesis": "GENESIS",
    "sega genesis": "GENESIS",
    "mega drive": "GENESIS",
    "megadrive": "GENESIS",
    "n64": "N64",
    "nintendo 64": "N64",
    "ps1": "PS1",
    "psx": "PS1",
    "playstation": "PS1",
    "playstation 1": "PS1",
    "ps2": "PS2",
    "playstation 2": "PS2",
    "ps3": "PS3",
    "playstation 3": "PS3",
    "psp": "PSP",
    "dreamcast": "DREAMCAST",
    "sega dreamcast": "DREAMCAST",
    "neogeo": "NEOGEO",
    "neo geo": "NEOGEO",
    "mame": "MAME",
    "arcade": "MAME",
    "gamecube": "GAMECUBE",
    "game cube": "GAMECUBE",
    "wii": "WII",
}

# Deliberately conservative: game/media formats only. BIOS, artwork, saves,
# cue-sheet companions such as .bin, and documentation are not auto-added.
_ROM_EXTENSIONS = {
    ".zip", ".7z",
    ".nes", ".fds",
    ".sfc", ".smc",
    ".gb", ".gbc", ".gba",
    ".nds",
    ".md", ".gen", ".smd",
    ".n64", ".z64", ".v64",
    ".cue", ".chd", ".pbp",
    ".iso", ".cso",
    ".gcm", ".rvz", ".wbfs",
}

_TRAILING_TAG_RE = re.compile(r"(?:\s*[\(\[][^)\]]+[\)\]])+$")


def _ensure_config():
    if not _CONFIG_PATH.exists() and _EXAMPLE_PATH.exists():
        shutil.copyfile(_EXAMPLE_PATH, _CONFIG_PATH)


def _parse_bool(value, default=True):
    text = str(value or "").strip().lower()
    if text in {"1", "true", "yes", "on"}:
        return True
    if text in {"0", "false", "no", "off"}:
        return False
    return default


def _expand_path(value):
    text = os.path.expandvars(os.path.expanduser(str(value or "").strip()))
    return Path(text) if text else None


def load_rom_roots(config_path=None):
    """Return enabled ROM roots from config/roms.ini."""
    path = Path(config_path) if config_path else _CONFIG_PATH
    if config_path is None:
        _ensure_config()

    config = configparser.ConfigParser()
    config.read(path, encoding="utf-8")

    roots = []
    for section in config.sections():
        item = config[section]
        if not _parse_bool(item.get("enabled", "true"), True):
            continue

        root = _expand_path(item.get("path", ""))
        if root:
            roots.append({
                "id": section,
                "path": root,
                "scan_subfolders": _parse_bool(
                    item.get("scan_subfolders", "true"), True
                ),
            })

    return roots


def _canonical_platform(folder_name):
    normalized = re.sub(r"[_\-]+", " ", str(folder_name or "").strip())
    normalized = re.sub(r"\s+", " ", normalized).casefold()
    return _PLATFORM_ALIASES.get(normalized)


def _display_name(path):
    # Keep internal punctuation, but remove common trailing region/revision tags.
    name = _TRAILING_TAG_RE.sub("", path.stem).strip()
    return name or path.stem


def _stable_rom_id(platform_name, path):
    try:
        normalized = str(path.resolve()).casefold()
    except OSError:
        normalized = str(path.absolute()).casefold()

    digest = hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:12].upper()
    return f"ROM_{platform_name}_{digest}"


def _game_from_rom(path, platform_name):
    name = _display_name(path)
    return {
        "id": _stable_rom_id(platform_name, path),
        "name": name,
        "title": name,
        "folder": platform_name,
        "platform": platform_name,
        "year": None,
        "genre": "",
        "developer": "",
        "publisher": "",
        "launch_type": "ROM",
        "path": str(path),
        "executable_path": "",
        "rom_path": str(path),
        # Empty means emulator resolution is platform-driven. A manual game
        # entry can still explicitly select a profile.
        "emulator": "",
        "steam_id": "",
        "favorite": False,
        "auto_discovered": True,
    }


def _iter_platform_folders(root):
    """Yield known platform directories under a configured ROM root."""
    try:
        children = sorted(
            (item for item in root.iterdir() if item.is_dir()),
            key=lambda item: item.name.casefold(),
        )
    except OSError:
        return

    for folder in children:
        platform_name = _canonical_platform(folder.name)
        if platform_name:
            yield folder, platform_name


def discover_rom_games(roots=None):
    """Scan configured ROM roots and return normal J-29 game records."""
    roots = roots if roots is not None else load_rom_roots()
    games = []
    seen_paths = set()

    for root_info in roots:
        root = Path(root_info["path"]).expanduser()
        if not root.is_dir():
            continue

        recursive = bool(root_info.get("scan_subfolders", True))

        for platform_folder, platform_name in _iter_platform_folders(root):
            try:
                files = (
                    platform_folder.rglob("*")
                    if recursive
                    else platform_folder.glob("*")
                )
                files = sorted(
                    (item for item in files if item.is_file()),
                    key=lambda item: str(item).casefold(),
                )
            except OSError:
                continue

            for rom_path in files:
                if rom_path.suffix.casefold() not in _ROM_EXTENSIONS:
                    continue

                try:
                    key = str(rom_path.resolve()).casefold()
                except OSError:
                    key = str(rom_path.absolute()).casefold()

                if key in seen_paths:
                    continue

                seen_paths.add(key)
                games.append(_game_from_rom(rom_path, platform_name))

    return games
