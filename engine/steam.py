"""Cross-platform Steam discovery helpers for J-29.

v0.24 keeps Steam-specific filesystem knowledge inside the engine so shells
only receive normal game metadata records.
"""

from __future__ import annotations

import os
import platform
import re
from pathlib import Path


_MANIFEST_RE = re.compile(r"appmanifest_(\d+)\.acf$", re.IGNORECASE)
_VDF_PAIR_RE = re.compile(r'^\s*"([^"]+)"\s+"([^"]*)"\s*$')

# Steam installs a handful of support packages beside normal games. Keep the
# filter deliberately conservative so J-29 does not hide legitimate software.
_EXCLUDED_APP_IDS = {
    "228980",  # Steamworks Common Redistributables
}

_EXCLUDED_EXACT_NAMES = {
    "steamworks common redistributables",
}


def _is_non_game_manifest(app_id: str, name: str) -> bool:
    """Return True only for Steam packages we explicitly know are not games."""
    if app_id.strip() in _EXCLUDED_APP_IDS:
        return True
    return name.strip().casefold() in _EXCLUDED_EXACT_NAMES



def _decode_vdf_path(value: str) -> str:
    # Valve's VDF files commonly escape Windows path separators.
    return value.replace("\\\\", "\\")


def _read_key_values(path: Path) -> dict[str, str]:
    """Read the simple quoted key/value pairs used by Steam ACF/VDF files."""
    values: dict[str, str] = {}

    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return values

    for line in text.splitlines():
        match = _VDF_PAIR_RE.match(line)
        if not match:
            continue
        key, value = match.groups()
        values[key.lower()] = value

    return values


def default_steam_roots() -> list[Path]:
    """Return likely Steam installation roots for the current OS."""
    home = Path.home()
    system = platform.system()
    candidates: list[Path] = []

    if system == "Windows":
        # Registry lookup catches custom Steam install locations while keeping
        # Windows-only code isolated inside the Steam integration module.
        try:
            import winreg

            registry_locations = [
                (winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam", "SteamPath"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam", "InstallPath"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Valve\Steam", "InstallPath"),
            ]

            for hive, key_path, value_name in registry_locations:
                try:
                    with winreg.OpenKey(hive, key_path) as key:
                        value, _ = winreg.QueryValueEx(key, value_name)
                    if value:
                        candidates.append(Path(value))
                except OSError:
                    pass
        except ImportError:
            pass

        for env_name in ("PROGRAMFILES(X86)", "PROGRAMFILES"):
            base = os.environ.get(env_name)
            if base:
                candidates.append(Path(base) / "Steam")

        # Common per-user/custom locations that cost almost nothing to check.
        candidates.extend([
            home / "AppData" / "Local" / "Steam",
            Path("C:/Steam"),
        ])

    elif system == "Darwin":
        candidates.append(home / "Library" / "Application Support" / "Steam")

    else:
        candidates.extend([
            home / ".local" / "share" / "Steam",
            home / ".steam" / "steam",
            home / ".var" / "app" / "com.valvesoftware.Steam" / ".local" / "share" / "Steam",
        ])

    # Preserve order while removing duplicate paths.
    unique: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        key = str(candidate.expanduser())
        if key not in seen:
            seen.add(key)
            unique.append(candidate.expanduser())

    return unique


def _library_paths_from_root(root: Path) -> list[Path]:
    """Return the Steam root plus any additional configured library folders."""
    libraries = [root]
    library_file = root / "steamapps" / "libraryfolders.vdf"

    try:
        text = library_file.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return libraries

    for line in text.splitlines():
        match = _VDF_PAIR_RE.match(line)
        if not match:
            continue

        key, value = match.groups()
        if key.lower() != "path":
            continue

        path = Path(_decode_vdf_path(value)).expanduser()
        if path not in libraries:
            libraries.append(path)

    return libraries


def find_steam_libraries(roots: list[Path] | None = None) -> list[Path]:
    """Find configured Steam library roots on Windows, Linux, and macOS."""
    roots = roots if roots is not None else default_steam_roots()
    libraries: list[Path] = []
    seen: set[str] = set()

    for root in roots:
        root = Path(root).expanduser()
        if not (root / "steamapps").is_dir():
            continue

        for library in _library_paths_from_root(root):
            if not (library / "steamapps").is_dir():
                continue
            key = str(library.resolve())
            if key not in seen:
                seen.add(key)
                libraries.append(library)

    return libraries


def _game_from_manifest(manifest: Path) -> dict | None:
    values = _read_key_values(manifest)

    app_id = values.get("appid", "").strip()
    if not app_id:
        match = _MANIFEST_RE.search(manifest.name)
        app_id = match.group(1) if match else ""

    name = values.get("name", "").strip()
    install_dir = values.get("installdir", "").strip()

    if not app_id or not name:
        return None

    if _is_non_game_manifest(app_id, name):
        return None

    library_root = manifest.parent.parent
    install_path = (
        library_root / "steamapps" / "common" / install_dir
        if install_dir
        else None
    )

    return {
        "id": f"STEAM_{app_id}",
        "name": name,
        "title": name,
        "folder": "STEAM",
        "platform": "PC",
        "year": None,
        "genre": "",
        "developer": "",
        "publisher": "",
        "launch_type": "STEAM",
        "path": "",
        "executable_path": "",
        "rom_path": "",
        "emulator": "",
        "steam_id": app_id,
        "steam_install_path": str(install_path) if install_path else "",
        "favorite": False,
    }


def discover_steam_games(roots: list[Path] | None = None) -> list[dict]:
    """Discover installed Steam titles and return normal J-29 game records."""
    games: list[dict] = []
    seen_app_ids: set[str] = set()

    for library in find_steam_libraries(roots):
        steamapps = library / "steamapps"

        try:
            manifests = sorted(steamapps.glob("appmanifest_*.acf"))
        except OSError:
            continue

        for manifest in manifests:
            game = _game_from_manifest(manifest)
            if not game:
                continue

            app_id = game["steam_id"]
            if app_id in seen_app_ids:
                continue

            seen_app_ids.add(app_id)
            games.append(game)

    return games
