import ctypes
import hashlib
import os
import platform
import string
from pathlib import Path



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
    """Return a v0.26 media descriptor for a mounted volume."""
    volume_root = Path(volume_root)
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
