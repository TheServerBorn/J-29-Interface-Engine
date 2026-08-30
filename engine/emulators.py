"""Cross-platform emulator profiles and ROM launch support for J-29."""

import configparser
import os
import platform
import shlex
import shutil
import subprocess
from pathlib import Path


_CONFIG_PATH = Path("config/emulators.ini")
_EXAMPLE_PATH = Path("config/emulators.example.ini")

# RetroArch libretro core filenames by J-29 platform.
# Profiles can use {core} in their arguments and J-29 will resolve it
# automatically from the game's platform.
_RETROARCH_CORES = {
    "SNES": "snes9x_libretro.dll",
    "NES": "mesen_libretro.dll",
    "GBC": "gambatte_libretro.dll",
    "GB": "gambatte_libretro.dll",
    "GBA": "mgba_libretro.dll",
    "GENESIS": "genesis_plus_gx_libretro.dll",
    "MEGADRIVE": "genesis_plus_gx_libretro.dll",
    "N64": "mupen64plus_next_libretro.dll",
    "NINTENDO 64": "mupen64plus_next_libretro.dll",
}

def _retroarch_core_path(executable, game):
    platform_name = str(game.get("platform", "") or "").strip().upper()
    core_name = _RETROARCH_CORES.get(platform_name)
    if not core_name:
        return None
    return str(Path(executable).parent / "cores" / core_name)



def _ensure_config():
    if not _CONFIG_PATH.exists() and _EXAMPLE_PATH.exists():
        shutil.copyfile(_EXAMPLE_PATH, _CONFIG_PATH)


def load_emulator_profiles():
    """Load emulator profiles keyed by their case-insensitive profile ID."""
    _ensure_config()
    config = configparser.ConfigParser()
    config.read(_CONFIG_PATH, encoding="utf-8")
    profiles = {}

    for section in config.sections():
        item = config[section]
        profiles[section.casefold()] = {
            "id": section,
            "name": item.get("name", section).strip(),
            "platforms": [
                value.strip().upper()
                for value in item.get("platforms", "").split(",")
                if value.strip()
            ],
            "executable": item.get("executable", "").strip(),
            "executable_windows": item.get("executable_windows", "").strip(),
            "executable_linux": item.get("executable_linux", "").strip(),
            "executable_macos": item.get("executable_macos", "").strip(),
            "arguments": item.get("arguments", '"{rom}"').strip(),
        }

    return profiles


def _platform_executable(profile):
    system = platform.system()
    key = {
        "Windows": "executable_windows",
        "Linux": "executable_linux",
        "Darwin": "executable_macos",
    }.get(system, "executable")
    return profile.get(key) or profile.get("executable", "")


def _resolve_executable(value):
    value = os.path.expandvars(os.path.expanduser(str(value or "").strip()))
    if not value:
        return None

    path = Path(value)
    if path.exists():
        return str(path)

    return shutil.which(value)


def find_profile(game, profiles=None):
    """Resolve an explicit emulator ID first, otherwise match the platform."""
    profiles = profiles or load_emulator_profiles()
    requested = str(game.get("emulator", "") or "").strip().casefold()

    if requested:
        return profiles.get(requested)

    platform_name = str(game.get("platform", "") or "").strip().upper()
    for profile in profiles.values():
        if platform_name and platform_name in profile["platforms"]:
            return profile

    return None


def launch_rom(game):
    """Launch a ROM through its configured emulator profile."""
    rom_value = game.get("rom_path") or game.get("path")
    rom_value = os.path.expandvars(os.path.expanduser(str(rom_value or "").strip()))
    if not rom_value:
        return False

    rom_path = Path(rom_value)
    if not rom_path.exists():
        return False

    profile = find_profile(game)
    if not profile:
        return False

    executable = _resolve_executable(_platform_executable(profile))
    if not executable:
        return False

    template = profile.get("arguments") or '"{rom}"'
    formatted = template.replace("{rom}", str(rom_path))

    if "{core}" in formatted:
        core_path = _retroarch_core_path(executable, game)
        if not core_path or not Path(core_path).exists():
            return False
        formatted = formatted.replace("{core}", core_path)

    try:
        # Parse the profile template into a clean argv list. subprocess.Popen
        # receives each argument separately, so surrounding quote characters
        # must not remain attached to Windows paths.
        args = shlex.split(formatted, posix=True)
        subprocess.Popen([executable, *args])
        return True
    except (OSError, ValueError):
        return False
