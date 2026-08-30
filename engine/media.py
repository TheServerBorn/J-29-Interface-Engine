import configparser
import ctypes
import hashlib
import os
import platform
import string
from pathlib import Path



# J-29 removable-media metadata format introduced in v0.27.
MEDIA_METADATA_FILENAME = "j29-media.ini"

def _media_descriptor_id(volume, title, rom_path):
    import hashlib
    seed = f"{volume}|{title}|{rom_path}".casefold()
    return hashlib.sha1(seed.encode("utf-8")).hexdigest()[:12].upper()

def read_media_metadata(volume):
    volume = Path(volume)
    descriptor = volume / MEDIA_METADATA_FILENAME
    if not descriptor.is_file():
        return None
    parser = configparser.ConfigParser()
    try:
        parser.read(descriptor, encoding="utf-8")
    except (OSError, configparser.Error):
        return {"valid": False, "reason": "INVALID MEDIA METADATA"}
    if not parser.has_section("J29_MEDIA"):
        return {"valid": False, "reason": "J29_MEDIA SECTION NOT FOUND"}

    section = parser["J29_MEDIA"]
    media_type = section.get("type", "GAME").strip().upper()
    title = section.get("title", "").strip()
    platform_name = section.get("platform", "").strip().upper()
    game_id = section.get("game_id", "").strip()
    rom_value = section.get("rom", "").strip()

    if media_type != "GAME":
        return {"valid": False, "reason": f"UNSUPPORTED MEDIA TYPE: {media_type}"}

    # Launch-key mode: the physical medium represents an existing J-29
    # library entry. This intentionally takes precedence if both fields exist.
    if game_id:
        game = {
            "id": "MEDIAKEY_" + _media_descriptor_id(volume, title or game_id, game_id),
            "name": title or game_id,
            "title": title or game_id,
            "folder": platform_name or "MEDIA",
            "platform": platform_name,
            "launch_type": "LIBRARY",
            "target_game_id": game_id,
            "favorite": False,
            "source": "PHYSICAL_MEDIA",
            "media_metadata": str(descriptor),
        }
        return {
            "valid": True,
            "type": media_type,
            "mode": "LAUNCH_KEY",
            "game": game,
        }

    if not title or not rom_value:
        return {
            "valid": False,
            "reason": "MEDIA METADATA REQUIRES GAME_ID OR TITLE AND ROM",
        }

    # Metadata files may be authored on a different OS, so accept either
    # slash style instead of interpreting the raw string as an OS-native Path.
    rom_parts = [part for part in rom_value.replace("\\", "/").split("/") if part]
    rom_path = volume.joinpath(*rom_parts).resolve()
    volume_resolved = volume.resolve()

    try:
        rom_path.relative_to(volume_resolved)
    except ValueError:
        return {
            "valid": False,
            "reason": "MEDIA ROM PATH OUTSIDE VOLUME",
            "requested_rom": rom_value,
            "resolved_rom": str(rom_path),
        }

    if not rom_path.is_file():
        return {
            "valid": False,
            "reason": "MEDIA ROM NOT FOUND",
            "requested_rom": rom_value,
            "resolved_rom": str(rom_path),
        }

    if not platform_name:
        platform_name = _platform_from_path(rom_path, volume) or "UNKNOWN"

    game = {
        "id": "MEDIA_" + _media_descriptor_id(volume, title, rom_path),
        "name": title, "title": title, "folder": platform_name,
        "platform": platform_name, "launch_type": "ROM",
        "rom_path": str(rom_path), "path": str(rom_path),
        "favorite": False, "source": "PHYSICAL_MEDIA",
        "media_metadata": str(descriptor),
    }
    return {
        "valid": True,
        "type": media_type,
        "mode": "SELF_CONTAINED",
        "game": game,
    }

# Keep v0.26 deliberately conservative. v0.27 will introduce the formal
# J-29 media metadata/container format.
_ROM_EXTENSIONS = {
    ".zip", ".7z",
    ".nes", ".fds",
    ".sfc", ".smc",
    ".gb", ".gbc", ".gba", ".nds",
    ".md", ".gen", ".smd",
    ".n64", ".z64", ".v64",
    ".cue", ".chd", ".pbp",
    ".iso", ".cso", ".gcm", ".rvz", ".wbfs",
}

_PLATFORM_FOLDERS = {
    "snes": "SNES",
    "super nintendo": "SNES",
    "nes": "NES",
    "nintendo": "NES",
    "gb": "GB",
    "game boy": "GB",
    "gbc": "GBC",
    "game boy color": "GBC",
    "gba": "GBA",
    "game boy advance": "GBA",
    "ds": "DS",
    "nintendo ds": "DS",
    "genesis": "GENESIS",
    "sega genesis": "GENESIS",
    "mega drive": "GENESIS",
    "megadrive": "GENESIS",
    "n64": "N64",
    "nintendo 64": "N64",
    "ps1": "PS1",
    "playstation 1": "PS1",
    "ps2": "PS2",
    "playstation 2": "PS2",
    "ps3": "PS3",
    "playstation 3": "PS3",
    "psp": "PSP",
    "playstation portable": "PSP",
    "dreamcast": "DREAMCAST",
    "neogeo": "NEOGEO",
    "neo geo": "NEOGEO",
    "mame": "MAME",
    "arcade": "MAME",
    "gamecube": "GAMECUBE",
    "game cube": "GAMECUBE",
    "wii": "WII",
}

_EXTENSION_PLATFORM_HINTS = {
    ".nes": "NES",
    ".fds": "NES",
    ".sfc": "SNES",
    ".smc": "SNES",
    ".gb": "GB",
    ".gbc": "GBC",
    ".gba": "GBA",
    ".nds": "DS",
    ".md": "GENESIS",
    ".gen": "GENESIS",
    ".smd": "GENESIS",
    ".n64": "N64",
    ".z64": "N64",
    ".v64": "N64",
    ".gcm": "GAMECUBE",
    ".rvz": "GAMECUBE",
    ".wbfs": "WII",
    ".pbp": "PS1",
}


def _windows_volumes():
    kernel32 = ctypes.windll.kernel32
    mask = kernel32.GetLogicalDrives()
    volumes = []

    for index, letter in enumerate(string.ascii_uppercase):
        if not (mask & (1 << index)):
            continue

        root = f"{letter}:\\"
        drive_type = kernel32.GetDriveTypeW(ctypes.c_wchar_p(root))

        # Ignore invalid/no-root, network and RAM drives. Keep fixed drives too:
        # many USB SSD/HDD devices report DRIVE_FIXED even though removable.
        if drive_type in (0, 1, 4, 6):
            continue

        path = Path(root)

        # Windows can keep a drive letter assigned to an empty USB/SD card
        # reader. "No Media" slots must not count as mounted media, otherwise
        # inserting a card into the same drive letter produces no new event.
        try:
            if not path.exists():
                continue

            # Touch the filesystem. An empty reader may have a logical drive
            # letter but no accessible mounted volume.
            next(path.iterdir(), None)
        except (OSError, PermissionError):
            continue

        volumes.append(path)

    return volumes


def _linux_volumes():
    roots = []
    username = os.environ.get("USER") or os.environ.get("USERNAME") or ""

    candidates = [
        Path("/media") / username,
        Path("/run/media") / username,
        Path("/mnt"),
    ]

    for parent in candidates:
        if not parent.is_dir():
            continue
        try:
            for child in parent.iterdir():
                if child.is_dir():
                    roots.append(child)
        except OSError:
            pass

    return roots


def _macos_volumes():
    parent = Path("/Volumes")
    if not parent.is_dir():
        return []

    try:
        return [p for p in parent.iterdir() if p.is_dir()]
    except OSError:
        return []


def _list_media_volumes_raw():
    system = platform.system()

    if system == "Windows":
        volumes = _windows_volumes()
        system_drive = os.environ.get("SystemDrive", "C:").rstrip("\\/").casefold()
        return [
            p for p in volumes
            if str(p).rstrip("\\/").casefold() != system_drive
        ]

    if system == "Darwin":
        return _macos_volumes()

    return _linux_volumes()



def list_media_volumes():
    return _list_media_volumes_raw()


def _windows_volume_signature(path):
    """Return a signature that changes when media inside a reader changes."""
    root = str(path)
    if not root.endswith("\\"):
        root += "\\"

    volume_name = ctypes.create_unicode_buffer(261)
    filesystem_name = ctypes.create_unicode_buffer(261)
    serial_number = ctypes.c_uint(0)
    max_component_length = ctypes.c_uint(0)
    filesystem_flags = ctypes.c_uint(0)

    ok = ctypes.windll.kernel32.GetVolumeInformationW(
        ctypes.c_wchar_p(root),
        volume_name,
        len(volume_name),
        ctypes.byref(serial_number),
        ctypes.byref(max_component_length),
        ctypes.byref(filesystem_flags),
        filesystem_name,
        len(filesystem_name),
    )

    if not ok:
        return None

    return (
        str(path).rstrip("\\/").casefold(),
        int(serial_number.value),
        volume_name.value.casefold(),
        filesystem_name.value.casefold(),
    )


def snapshot_media():
    snapshot = {}

    for path in list_media_volumes():
        if platform.system() == "Windows":
            key = _windows_volume_signature(path)
            if key is None:
                continue
        else:
            key = _volume_key(path)

        snapshot[key] = path

    return snapshot


def _volume_key(path):
    try:
        return str(path.resolve()).casefold()
    except OSError:
        return str(path).casefold()


def newly_inserted_media(previous_snapshot):
    current = snapshot_media()
    inserted = [
        path
        for key, path in current.items()
        if key not in previous_snapshot
    ]
    return inserted, current


def _clean_title(path):
    title = path.stem

    # Strip common ROM region/revision trailers while keeping the real title.
    title = re_sub_trailer(title)
    return title.strip() or path.stem


def re_sub_trailer(title):
    import re
    previous = None
    value = title
    pattern = re.compile(r"\s*[\(\[].*?[\)\]]\s*$")

    while value != previous:
        previous = value
        value = pattern.sub("", value)

    return value


def _platform_from_path(path, volume_root):
    try:
        relatives = path.relative_to(volume_root).parts[:-1]
    except ValueError:
        relatives = path.parts[:-1]

    for part in reversed(relatives):
        mapped = _PLATFORM_FOLDERS.get(part.strip().casefold())
        if mapped:
            return mapped

    return _EXTENSION_PLATFORM_HINTS.get(path.suffix.lower(), "")


def _candidate_files(volume_root, max_files=2000):
    candidates = []
    examined = 0

    try:
        for path in volume_root.rglob("*"):
            if examined >= max_files:
                break
            examined += 1

            try:
                if not path.is_file():
                    continue
            except OSError:
                continue

            if path.suffix.lower() in _ROM_EXTENSIONS:
                candidates.append(path)
    except OSError:
        pass

    return candidates


def inspect_media(volume_root):
    """Return a physical-media descriptor for a mounted volume."""
    volume_root = Path(volume_root)

    metadata = read_media_metadata(volume_root)
    if metadata is not None:
        return {
            "volume": str(volume_root),
            "volume_name": volume_root.name or str(volume_root),
            "candidate_count": 1 if metadata.get("valid") else 0,
            "game": metadata.get("game"),
            "metadata": metadata,
            "detection_method": "J29_METADATA",
        }

    candidates = _candidate_files(volume_root)

    descriptor = {
        "volume": str(volume_root),
        "volume_name": volume_root.name or str(volume_root),
        "game": None,
        "candidate_count": len(candidates),
    }

    # v0.26 intentionally prompts only when the media represents one obvious
    # game. Collections/multi-game media belong to v0.27.
    if len(candidates) != 1:
        return descriptor

    rom = candidates[0]
    platform_name = _platform_from_path(rom, volume_root)
    digest = hashlib.sha1(str(rom).encode("utf-8")).hexdigest()[:12].upper()

    descriptor["game"] = {
        "id": f"MEDIA_{digest}",
        "name": _clean_title(rom).upper(),
        "title": _clean_title(rom),
        "folder": platform_name or "MEDIA",
        "platform": platform_name,
        "launch_type": "ROM",
        "rom_path": str(rom),
        "path": str(rom),
        "emulator": "",
        "favorite": False,
        "source": "PHYSICAL_MEDIA",
    }

    return descriptor


class MediaMonitor:
    """Track insertions/removals without leaking OS-specific details to shells."""

    def __init__(self):
        self._snapshot = snapshot_media()

    def poll(self):
        current = snapshot_media()
        previous_keys = set(self._snapshot)
        current_keys = set(current)

        inserted_keys = current_keys - previous_keys
        removed_keys = previous_keys - current_keys


        inserted = [
            inspect_media(current[key])
            for key in sorted(inserted_keys)
        ]
        removed = [
            {
                "volume": str(self._snapshot[key]),
                "volume_name": self._snapshot[key].name or str(self._snapshot[key]),
            }
            for key in sorted(removed_keys)
        ]


        self._snapshot = current
        return {
            "inserted": inserted,
            "removed": removed,
        }
