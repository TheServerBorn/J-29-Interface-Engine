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

# RetroArch core candidates by J-29 platform, in preferred order.
#
# J-29 inspects the actual RetroArch cores directory and selects the first
# installed compatible core instead of assuming a single exact core package.
_RETROARCH_CORE_CANDIDATES = {
    "SNES": (
        "snes9x_libretro",
        "snes9x_current_libretro",
        "bsnes_libretro",
        "bsnes_hd_beta_libretro",
    ),
    "NES": (
        "mesen_libretro",
        "fceumm_libretro",
        "nestopia_libretro",
        "quicknes_libretro",
    ),
    "GB": (
        "gambatte_libretro",
        "sameboy_libretro",
        "gearboy_libretro",
        "tgbdual_libretro",
    ),
    "GBC": (
        "gambatte_libretro",
        "sameboy_libretro",
        "gearboy_libretro",
        "tgbdual_libretro",
    ),
    "GBA": (
        "mgba_libretro",
        "vbam_libretro",
        "vba_next_libretro",
        "gpsp_libretro",
    ),
    "GENESIS": (
        "genesis_plus_gx_libretro",
        "genesis_plus_gx_wide_libretro",
        "picodrive_libretro",
        "blastem_libretro",
    ),
    "MEGADRIVE": (
        "genesis_plus_gx_libretro",
        "genesis_plus_gx_wide_libretro",
        "picodrive_libretro",
        "blastem_libretro",
    ),
    "N64": (
        "mupen64plus_next_libretro",
        "parallel_n64_libretro",
    ),
    "NINTENDO 64": (
        "mupen64plus_next_libretro",
        "parallel_n64_libretro",
    ),
    "PS1": (
        "swanstation_libretro",
        "beetle_psx_hw_libretro",
        "beetle_psx_libretro",
        "pcsx_rearmed_libretro",
    ),
    "DS": (
        "melonds_libretro",
        "desmume_libretro",
        "desmume2015_libretro",
    ),
    "DREAMCAST": (
        "flycast_libretro",
    ),
    "NEOGEO": (
        "fbneo_libretro",
        "mame_libretro",
        "mame_current_libretro",
        "mame2003_plus_libretro",
    ),
    "MAME": (
        "mame_libretro",
        "mame_current_libretro",
        "fbneo_libretro",
        "mame2003_plus_libretro",
        "mame2003_libretro",
    ),
}

_CORE_SUFFIXES = {
    "Windows": ".dll",
    "Linux": ".so",
    "Darwin": ".dylib",
}


def _core_suffix():
    return _CORE_SUFFIXES.get(platform.system(), "")


def _retroarch_core_directory(executable):
    return Path(executable).parent / "cores"


def get_installed_retroarch_cores(executable):
    """Return installed RetroArch core filenames keyed case-insensitively."""
    core_dir = _retroarch_core_directory(executable)
    if not core_dir.is_dir():
        return {}

    installed = {}
    try:
        for item in core_dir.iterdir():
            if item.is_file():
                installed[item.name.casefold()] = item
    except OSError:
        return {}

    return installed


def _candidate_filename(base_name):
    suffix = _core_suffix()
    if suffix and not base_name.casefold().endswith(suffix.casefold()):
        return base_name + suffix
    return base_name


def resolve_retroarch_core(executable, game):
    """Resolve the first installed compatible RetroArch core.

    Returns (core_path, diagnostic). core_path is None when J-29 cannot
    resolve a suitable installed core.
    """
    platform_name = str(game.get("platform", "") or "").strip().upper()
    candidates = _RETROARCH_CORE_CANDIDATES.get(platform_name)

    if not candidates:
        return None, f"NO CORE PROFILE FOR {platform_name or 'UNKNOWN PLATFORM'}"

    installed = get_installed_retroarch_cores(executable)
    if not installed:
        return None, "RETROARCH CORES NOT FOUND"

    for base_name in candidates:
        filename = _candidate_filename(base_name)
        match = installed.get(filename.casefold())
        if match:
            return str(match), f"CORE {match.name}"

    expected = ", ".join(_candidate_filename(name) for name in candidates[:3])
    return None, f"CORE NOT INSTALLED: {expected}"


# Standalone emulator candidates for platforms that should not depend on
# RetroArch. J-29 resolves these by platform and searches common install paths
# plus PATH. The first available candidate wins.
_STANDALONE_EMULATORS = {
    "PS2": (
        {
            "id": "PCSX2",
            "name": "PCSX2",
            "windows": (
                r"%LOCALAPPDATA%\Programs\PCSX2\pcsx2-qt.exe",
                r"%PROGRAMFILES%\PCSX2\pcsx2-qt.exe",
                r"%PROGRAMFILES(X86)%\PCSX2\pcsx2-qt.exe",
                r"D:\PCSX2\pcsx2-qt.exe",
                "pcsx2-qt.exe",
                "pcsx2.exe",
            ),
            "linux": ("pcsx2-qt", "pcsx2"),
            "darwin": (
                "/Applications/PCSX2.app/Contents/MacOS/PCSX2-Qt",
                "/Applications/PCSX2.app/Contents/MacOS/pcsx2-qt",
            ),
            "arguments": '"{rom}"',
        },
    ),
    "PS3": (
        {
            "id": "RPCS3",
            "name": "RPCS3",
            "windows": (
                r"%LOCALAPPDATA%\rpcs3\rpcs3.exe",
                r"%PROGRAMFILES%\RPCS3\rpcs3.exe",
                r"D:\RPCS3\rpcs3.exe",
                "rpcs3.exe",
            ),
            "linux": ("rpcs3",),
            "darwin": (
                "/Applications/RPCS3.app/Contents/MacOS/rpcs3",
            ),
            "arguments": '"{rom}"',
        },
    ),
    "GAMECUBE": (
        {
            "id": "DOLPHIN",
            "name": "Dolphin",
            "windows": (
                r"%PROGRAMFILES%\Dolphin\Dolphin.exe",
                r"%PROGRAMFILES(X86)%\Dolphin\Dolphin.exe",
                r"D:\Dolphin\Dolphin.exe",
                "Dolphin.exe",
            ),
            "linux": ("dolphin-emu", "dolphin"),
            "darwin": (
                "/Applications/Dolphin.app/Contents/MacOS/Dolphin",
            ),
            "arguments": '-b -e "{rom}"',
        },
    ),
    "WII": (
        {
            "id": "DOLPHIN",
            "name": "Dolphin",
            "windows": (
                r"%PROGRAMFILES%\Dolphin\Dolphin.exe",
                r"%PROGRAMFILES(X86)%\Dolphin\Dolphin.exe",
                r"D:\Dolphin\Dolphin.exe",
                "Dolphin.exe",
            ),
            "linux": ("dolphin-emu", "dolphin"),
            "darwin": (
                "/Applications/Dolphin.app/Contents/MacOS/Dolphin",
            ),
            "arguments": '-b -e "{rom}"',
        },
    ),
    "PSP": (
        {
            "id": "PPSSPP",
            "name": "PPSSPP",
            "windows": (
                r"%PROGRAMFILES%\PPSSPP\PPSSPPWindows64.exe",
                r"%PROGRAMFILES(X86)%\PPSSPP\PPSSPPWindows64.exe",
                r"D:\PPSSPP\PPSSPPWindows64.exe",
                "PPSSPPWindows64.exe",
                "PPSSPPWindows.exe",
            ),
            "linux": ("PPSSPPSDL", "ppsspp"),
            "darwin": (
                "/Applications/PPSSPP.app/Contents/MacOS/PPSSPP",
            ),
            "arguments": '"{rom}"',
        },
    ),
}


def _platform_candidate_paths(candidate):
    system = platform.system()
    if system == "Windows":
        return candidate.get("windows", ())
    if system == "Darwin":
        return candidate.get("darwin", ())
    return candidate.get("linux", ())


def _resolve_candidate_executable(value):
    expanded = os.path.expandvars(os.path.expanduser(str(value or "").strip()))
    if not expanded:
        return None

    path = Path(expanded)
    if path.is_file():
        return str(path)

    found = shutil.which(expanded)
    if found:
        return found

    # shutil.which can also resolve simple basename candidates while path
    # expansion above handles configured absolute/common paths.
    if path.name == expanded:
        found = shutil.which(path.name)
        if found:
            return found

    return None


def resolve_standalone_emulator(game):
    """Return a detected standalone emulator profile for the game's platform."""
    platform_name = str(game.get("platform", "") or "").strip().upper()
    candidates = _STANDALONE_EMULATORS.get(platform_name, ())

    for candidate in candidates:
        for executable_candidate in _platform_candidate_paths(candidate):
            executable = _resolve_candidate_executable(executable_candidate)
            if executable:
                return {
                    "id": candidate["id"],
                    "name": candidate["name"],
                    "executable": executable,
                    "arguments": candidate["arguments"],
                    "platform": platform_name,
                }

    return None


def standalone_support_status(game):
    platform_name = str(game.get("platform", "") or "").strip().upper()
    candidates = _STANDALONE_EMULATORS.get(platform_name, ())
    if not candidates:
        return False, f"NO STANDALONE EMULATOR PROFILE FOR {platform_name or 'UNKNOWN PLATFORM'}"

    names = ", ".join(candidate["name"] for candidate in candidates)
    return False, f"EMULATOR NOT INSTALLED: {names}"



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


def _launch_with_template(executable, template, rom_path, game):
    formatted = template.replace("{rom}", str(rom_path))

    if "{core}" in formatted:
        core_path, core_detail = resolve_retroarch_core(executable, game)
        if not core_path:
            return False, core_detail
        formatted = formatted.replace("{core}", core_path)

    try:
        args = shlex.split(formatted, posix=True)
        subprocess.Popen([executable, *args])
        return True, "PROGRAM LAUNCHED"
    except ValueError:
        return False, "INVALID EMULATOR ARGUMENTS"
    except OSError as exc:
        return False, f"EMULATOR LAUNCH FAILED: {exc.__class__.__name__}"


def launch_rom_with_status(game):
    """Launch a ROM using explicit, standalone, or RetroArch resolution."""
    rom_value = game.get("rom_path") or game.get("path")
    rom_value = os.path.expandvars(os.path.expanduser(str(rom_value or "").strip()))
    if not rom_value:
        return False, "ROM PATH NOT CONFIGURED"

    rom_path = Path(rom_value)
    if not rom_path.exists():
        return False, "ROM FILE NOT FOUND"

    # 1. Explicit emulator profile always wins.
    explicit_emulator = str(game.get("emulator", "") or "").strip()
    if explicit_emulator:
        profile = find_profile(game)
        if not profile:
            return False, f"EMULATOR PROFILE NOT FOUND: {explicit_emulator}"

        executable = _resolve_executable(_platform_executable(profile))
        if not executable:
            return False, f"EMULATOR NOT FOUND: {profile.get('name') or profile.get('id')}"

        template = profile.get("arguments") or '"{rom}"'
        return _launch_with_template(executable, template, rom_path, game)

    platform_name = str(game.get("platform", "") or "").strip().upper()

    # 2. Dedicated standalone emulators for platforms where they are preferred.
    if platform_name in _STANDALONE_EMULATORS:
        standalone = resolve_standalone_emulator(game)
        if not standalone:
            return standalone_support_status(game)

        return _launch_with_template(
            standalone["executable"],
            standalone["arguments"],
            rom_path,
            game,
        )

    # 3. Otherwise use a matching configured profile, typically RetroArch.
    profile = find_profile(game)
    if not profile:
        return False, f"NO EMULATOR PROFILE FOR {platform_name or 'UNKNOWN'}"

    executable = _resolve_executable(_platform_executable(profile))
    if not executable:
        return False, f"EMULATOR NOT FOUND: {profile.get('name') or profile.get('id')}"

    template = profile.get("arguments") or '"{rom}"'
    return _launch_with_template(executable, template, rom_path, game)


def launch_rom(game):
    """Backward-compatible boolean ROM launch helper."""
    launched, _detail = launch_rom_with_status(game)
    return launched
