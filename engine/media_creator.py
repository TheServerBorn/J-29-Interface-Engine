"""J-29 physical-media authoring helpers.

v0.29 writes the same j29-media.ini format that the v0.27 reader already
understands. Creator safety is intentionally stricter than normal media
recognition: only clearly removable/writable mount locations are eligible for
writes and the system volume is always rejected. Existing J-29 descriptors
require an explicit two-step replacement workflow; unrelated media files are
never modified by the creator.
"""

from configparser import ConfigParser
import ctypes
from io import StringIO
import os
import platform
from pathlib import Path
import tempfile


MEDIA_SECTION = "J29_MEDIA"
MEDIA_METADATA_FILENAME = "j29-media.ini"
SUPPORTED_TARGET_LAUNCH_TYPES = {"EXECUTABLE", "ROM", "STEAM"}


class MediaCreatorError(ValueError):
    """Raised when a library record or target cannot safely become J-29 media."""


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
    # that must itself remain inserted. The creator should target the normal
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
    launch_type = _clean(game.get("launch_type")).upper()
    game_id_upper = game_id.upper()
    folder_name = _clean(game.get("folder")).upper()

    if launch_type == "STEAM" or game_id_upper.startswith("STEAM_") or folder_name == "STEAM":
        platform_name = "STEAM"
    else:
        platform_name = _clean(
            game.get("platform") or game.get("folder") or "MEDIA"
        ).upper()

    return {
        "type": "GAME",
        "title": title,
        "platform": platform_name,
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
        "game_id": fields["game_id"],
        "status": status,
        "descriptor": descriptor,
    }




def _collection_games(games):
    """Return a validated, de-duplicated ordered collection selection."""
    ordered = []
    seen = set()

    for game in games or []:
        if not is_launch_key_eligible(game):
            raise MediaCreatorError("COLLECTION CONTAINS AN INELIGIBLE PROGRAM")

        game_id = _clean(game.get("id"))
        key = game_id.casefold()
        if key in seen:
            continue
        seen.add(key)
        ordered.append(game)

    if len(ordered) < 2:
        raise MediaCreatorError("COLLECTION REQUIRES AT LEAST TWO PROGRAMS")

    return ordered


def build_collection_descriptor(games, title):
    """Build an ordered metadata-only COLLECTION descriptor."""
    ordered = _collection_games(games)
    collection_title = _clean(title) or "J-29 COLLECTION"

    parser = ConfigParser()
    parser.optionxform = str.lower
    parser[MEDIA_SECTION] = {
        "type": "COLLECTION",
        "title": collection_title,
    }

    for index, game in enumerate(ordered, start=1):
        fields = _launch_key_fields(game)
        parser[f"ITEM_{index}"] = {
            "title": fields["title"],
            "platform": fields["platform"],
            "game_id": fields["game_id"],
        }

    buffer = StringIO()
    parser.write(buffer, space_around_delimiters=False)
    return buffer.getvalue().strip() + "\n"


def validate_collection_descriptor(text):
    """Validate creator-generated collection metadata before writing it."""
    parser = ConfigParser()
    try:
        parser.read_string(str(text or ""))
    except Exception as exc:
        return False, f"INVALID MEDIA METADATA: {exc}"

    if not parser.has_section(MEDIA_SECTION):
        return False, "J29_MEDIA SECTION NOT FOUND"

    section = parser[MEDIA_SECTION]
    if section.get("type", "").strip().upper() != "COLLECTION":
        return False, "MEDIA TYPE MUST BE COLLECTION"
    if not section.get("title", "").strip():
        return False, "COLLECTION TITLE NOT PROVIDED"

    item_sections = [
        name for name in parser.sections()
        if name.strip().upper().startswith(("ITEM_", "COLLECTION_ITEM_"))
    ]
    if len(item_sections) < 2:
        return False, "COLLECTION REQUIRES AT LEAST TWO ITEMS"

    seen = set()
    for index, name in enumerate(item_sections, start=1):
        item = parser[name]
        game_id = item.get("game_id", "").strip()
        if not game_id:
            return False, f"COLLECTION ITEM {index} HAS NO GAME ID"
        key = game_id.casefold()
        if key in seen:
            return False, f"COLLECTION ITEM {index} DUPLICATES A GAME ID"
        seen.add(key)

    return True, "READY"


def preview_collection(games, title):
    """Return user-facing collection preview data plus descriptor text."""
    ordered = _collection_games(games)
    collection_title = _clean(title) or "J-29 COLLECTION"
    descriptor = build_collection_descriptor(ordered, collection_title)
    valid, status = validate_collection_descriptor(descriptor)

    if not valid:
        raise MediaCreatorError(status)

    items = []
    for game in ordered:
        fields = _launch_key_fields(game)
        items.append({
            "title": fields["title"],
            "platform": fields["platform"],
            "game_id": fields["game_id"],
        })

    return {
        "media_type": "SOFTWARE COLLECTION",
        "title": collection_title,
        "item_count": len(items),
        "items": items,
        "target": "LIBRARY PROGRAMS",
        "status": status,
        "descriptor": descriptor,
    }


def _path_key(path):
    value = str(path or "").rstrip("\\/")
    if platform.system() == "Windows":
        return value.casefold()
    try:
        return str(Path(value).resolve())
    except (OSError, ValueError):
        return value


def _is_system_target(path):
    path = Path(path)
    system = platform.system()

    if system == "Windows":
        system_drive = os.environ.get("SystemDrive", "C:")
        return _path_key(path) == _path_key(system_drive)

    try:
        return path.resolve() == Path("/").resolve()
    except OSError:
        return str(path) == "/"


def _windows_volume_label(root):
    volume_name = ctypes.create_unicode_buffer(261)
    filesystem_name = ctypes.create_unicode_buffer(261)
    serial_number = ctypes.c_uint(0)
    max_component_length = ctypes.c_uint(0)
    filesystem_flags = ctypes.c_uint(0)

    ok = ctypes.windll.kernel32.GetVolumeInformationW(
        ctypes.c_wchar_p(str(root)),
        volume_name,
        len(volume_name),
        ctypes.byref(serial_number),
        ctypes.byref(max_component_length),
        ctypes.byref(filesystem_flags),
        filesystem_name,
        len(filesystem_name),
    )
    return volume_name.value.strip() if ok else ""


def _windows_creator_targets():
    """Return only DRIVE_REMOVABLE targets; fixed disks are too ambiguous to write."""
    import string

    kernel32 = ctypes.windll.kernel32
    mask = kernel32.GetLogicalDrives()
    targets = []

    for index, letter in enumerate(string.ascii_uppercase):
        if not (mask & (1 << index)):
            continue

        root = f"{letter}:\\"
        drive_type = kernel32.GetDriveTypeW(ctypes.c_wchar_p(root))

        # DRIVE_REMOVABLE only. Some USB SSD/HDD devices report DRIVE_FIXED;
        # those remain readable by J-29 but are intentionally not writable by
        # the creator until a stronger device-identity check is implemented.
        if drive_type != 2:
            continue

        path = Path(root)
        if _is_system_target(path):
            continue

        try:
            if not path.exists():
                continue
            next(path.iterdir(), None)
        except (OSError, PermissionError):
            continue

        label = _windows_volume_label(root)
        targets.append(_target_record(path, label, "REMOVABLE"))

    return targets


def _linux_creator_targets():
    username = os.environ.get("USER") or os.environ.get("USERNAME") or ""
    parents = [Path("/media") / username, Path("/run/media") / username]
    targets = []

    for parent in parents:
        if not parent.is_dir():
            continue
        try:
            children = list(parent.iterdir())
        except OSError:
            continue
        for child in children:
            if child.is_dir() and not _is_system_target(child):
                targets.append(_target_record(child, child.name, "REMOVABLE MOUNT"))

    return targets


def _macos_creator_targets():
    parent = Path("/Volumes")
    if not parent.is_dir():
        return []

    targets = []
    try:
        children = list(parent.iterdir())
    except OSError:
        return []

    for child in children:
        if child.is_dir() and not _is_system_target(child):
            targets.append(_target_record(child, child.name, "REMOVABLE VOLUME"))
    return targets


def _target_record(path, label, device_class):
    path = Path(path)
    descriptor = path / MEDIA_METADATA_FILENAME
    return {
        "path": str(path),
        "label": _clean(label),
        "device_class": device_class,
        "existing_descriptor": descriptor.is_file(),
        "writable": os.access(path, os.W_OK),
    }


def list_safe_media_targets():
    """Discover conservative creator targets without exposing system/fixed disks."""
    system = platform.system()
    if system == "Windows":
        targets = _windows_creator_targets()
    elif system == "Darwin":
        targets = _macos_creator_targets()
    else:
        targets = _linux_creator_targets()

    # De-duplicate and keep presentation stable.
    unique = {}
    for target in targets:
        if not target.get("writable"):
            continue
        unique[_path_key(target["path"])] = target

    return sorted(unique.values(), key=lambda item: _path_key(item["path"]))


def _resolve_safe_target(target_path):
    requested_key = _path_key(target_path)
    if not requested_key:
        raise MediaCreatorError("TARGET MEDIA NOT PROVIDED")

    if _is_system_target(target_path):
        raise MediaCreatorError("SYSTEM DRIVE CANNOT BE USED AS CREATOR TARGET")

    for candidate in list_safe_media_targets():
        if _path_key(candidate["path"]) == requested_key:
            return candidate

    raise MediaCreatorError("TARGET IS NOT A SAFE WRITABLE REMOVABLE VOLUME")


def write_launch_key_to_target(game, target_path):
    """Create a new j29-media.ini on a validated removable target.

    This checkpoint deliberately refuses to overwrite an existing descriptor.
    After writing, the file is parsed by the existing v0.27 reader to verify
    compatibility before success is reported.
    """
    fields = _launch_key_fields(game)
    descriptor_text = build_launch_key_descriptor(game)
    valid, status = validate_launch_key_descriptor(descriptor_text)
    if not valid:
        raise MediaCreatorError(status)

    target = _resolve_safe_target(target_path)
    root = Path(target["path"])
    descriptor_path = root / MEDIA_METADATA_FILENAME

    if descriptor_path.exists():
        raise MediaCreatorError("TARGET ALREADY CONTAINS J-29 MEDIA METADATA")

    created = False
    try:
        # Exclusive creation is the safety boundary: even if another process
        # creates the file after discovery, J-29 will not overwrite it.
        with descriptor_path.open("x", encoding="utf-8", newline="\n") as handle:
            created = True
            handle.write(descriptor_text)
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError as exc:
        raise MediaCreatorError("TARGET ALREADY CONTAINS J-29 MEDIA METADATA") from exc
    except OSError as exc:
        if created:
            try:
                descriptor_path.unlink(missing_ok=True)
            except OSError:
                pass
        raise MediaCreatorError(f"MEDIA WRITE FAILED: {exc}") from exc

    # Verify with the reader users already rely on, not a second creator-only
    # parser. A failed verification rolls back the descriptor we just created.
    from engine.media import read_media_metadata

    metadata = read_media_metadata(root)
    verified = bool(
        metadata
        and metadata.get("valid")
        and metadata.get("mode") == "LAUNCH_KEY"
        and (metadata.get("game") or {}).get("target_game_id") == fields["game_id"]
    )

    if not verified:
        try:
            descriptor_path.unlink(missing_ok=True)
        except OSError:
            pass
        raise MediaCreatorError("WRITE VERIFICATION FAILED; DESCRIPTOR REMOVED")

    return {
        "success": True,
        "target_path": str(root),
        "descriptor_path": str(descriptor_path),
        "title": fields["title"],
        "platform": fields["platform"],
        "game_id": fields["game_id"],
        "verified": True,
    }

def write_collection_to_target(games, title, target_path):
    """Create and verify a metadata-only J-29 collection on removable media.

    Overwrite remains deliberately disabled. Verification is performed through
    the existing v0.27 media reader and confirms collection item order as well
    as stable library IDs.
    """
    ordered = _collection_games(games)
    collection_title = _clean(title) or "J-29 COLLECTION"
    descriptor_text = build_collection_descriptor(ordered, collection_title)
    valid, status = validate_collection_descriptor(descriptor_text)
    if not valid:
        raise MediaCreatorError(status)

    expected_ids = [_launch_key_fields(game)["game_id"] for game in ordered]
    target = _resolve_safe_target(target_path)
    root = Path(target["path"])
    descriptor_path = root / MEDIA_METADATA_FILENAME

    if descriptor_path.exists():
        raise MediaCreatorError("TARGET ALREADY CONTAINS J-29 MEDIA METADATA")

    created = False
    try:
        with descriptor_path.open("x", encoding="utf-8", newline="\n") as handle:
            created = True
            handle.write(descriptor_text)
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError as exc:
        raise MediaCreatorError("TARGET ALREADY CONTAINS J-29 MEDIA METADATA") from exc
    except OSError as exc:
        if created:
            try:
                descriptor_path.unlink(missing_ok=True)
            except OSError:
                pass
        raise MediaCreatorError(f"MEDIA WRITE FAILED: {exc}") from exc

    from engine.media import read_media_metadata

    metadata = read_media_metadata(root)
    actual_ids = []
    if metadata and metadata.get("valid") and metadata.get("mode") == "COLLECTION":
        actual_ids = [
            (item or {}).get("target_game_id", "")
            for item in metadata.get("items", [])
        ]

    verified = bool(
        metadata
        and metadata.get("valid")
        and metadata.get("mode") == "COLLECTION"
        and metadata.get("title") == collection_title
        and actual_ids == expected_ids
    )

    if not verified:
        try:
            descriptor_path.unlink(missing_ok=True)
        except OSError:
            pass
        raise MediaCreatorError("WRITE VERIFICATION FAILED; DESCRIPTOR REMOVED")

    return {
        "success": True,
        "target_path": str(root),
        "descriptor_path": str(descriptor_path),
        "title": collection_title,
        "item_count": len(expected_ids),
        "game_ids": expected_ids,
        "verified": True,
    }


def inspect_existing_media(target_path):
    """Return a safe user-facing summary of an existing J-29 descriptor."""
    target = _resolve_safe_target(target_path)
    root = Path(target["path"])
    descriptor_path = root / MEDIA_METADATA_FILENAME

    if not descriptor_path.is_file():
        return {
            "exists": False,
            "valid": False,
            "target_path": str(root),
            "descriptor_path": str(descriptor_path),
            "mode": "NONE",
            "title": "",
            "reason": "NO J-29 METADATA FOUND",
        }

    from engine.media import read_media_metadata

    metadata = read_media_metadata(root)
    if not metadata or not metadata.get("valid"):
        return {
            "exists": True,
            "valid": False,
            "target_path": str(root),
            "descriptor_path": str(descriptor_path),
            "mode": "INVALID",
            "title": "UNREADABLE J-29 METADATA",
            "reason": (metadata or {}).get("reason", "INVALID MEDIA METADATA"),
        }

    mode = metadata.get("mode", "UNKNOWN")
    summary = {
        "exists": True,
        "valid": True,
        "target_path": str(root),
        "descriptor_path": str(descriptor_path),
        "mode": mode,
        "title": metadata.get("title", ""),
        "platform": "",
        "item_count": 0,
        "reason": "",
    }

    if mode in ("LAUNCH_KEY", "SELF_CONTAINED"):
        game = metadata.get("game") or {}
        summary["title"] = game.get("title") or game.get("name") or "J-29 GAME MEDIA"
        summary["platform"] = game.get("platform") or game.get("folder") or ""
    elif mode == "COLLECTION":
        summary["title"] = metadata.get("title") or "SOFTWARE COLLECTION"
        summary["item_count"] = len(metadata.get("items") or [])

    return summary


def _verify_launch_key_write(root, fields):
    from engine.media import read_media_metadata

    metadata = read_media_metadata(root)
    return bool(
        metadata
        and metadata.get("valid")
        and metadata.get("mode") == "LAUNCH_KEY"
        and (metadata.get("game") or {}).get("target_game_id") == fields["game_id"]
    )


def _verify_collection_write(root, collection_title, expected_ids):
    from engine.media import read_media_metadata

    metadata = read_media_metadata(root)
    actual_ids = []
    if metadata and metadata.get("valid") and metadata.get("mode") == "COLLECTION":
        actual_ids = [
            (item or {}).get("target_game_id", "")
            for item in metadata.get("items", [])
        ]

    return bool(
        metadata
        and metadata.get("valid")
        and metadata.get("mode") == "COLLECTION"
        and metadata.get("title") == collection_title
        and actual_ids == expected_ids
    )


def _restore_descriptor(root, descriptor_path, original_bytes):
    """Atomically restore the exact original descriptor bytes."""
    restore_name = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=str(root),
            prefix=".j29-media-restore-",
            suffix=".tmp",
            delete=False,
        ) as handle:
            restore_name = handle.name
            handle.write(original_bytes)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(restore_name, descriptor_path)
        restore_name = None
    finally:
        if restore_name:
            try:
                Path(restore_name).unlink(missing_ok=True)
            except OSError:
                pass


def _replace_descriptor_atomically(descriptor_text, target_path, verify_callback):
    """Replace only j29-media.ini and restore the original on verify failure."""
    target = _resolve_safe_target(target_path)
    root = Path(target["path"])
    descriptor_path = root / MEDIA_METADATA_FILENAME

    if not descriptor_path.is_file():
        raise MediaCreatorError("TARGET DOES NOT CONTAIN J-29 MEDIA METADATA")

    try:
        original_bytes = descriptor_path.read_bytes()
    except OSError as exc:
        raise MediaCreatorError(f"EXISTING METADATA COULD NOT BE READ: {exc}") from exc

    temp_name = None
    replaced = False
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            dir=str(root),
            prefix=".j29-media-write-",
            suffix=".tmp",
            delete=False,
            encoding="utf-8",
            newline="\n",
        ) as handle:
            temp_name = handle.name
            handle.write(descriptor_text)
            handle.flush()
            os.fsync(handle.fileno())

        # Same-volume os.replace gives us an atomic descriptor swap. No other
        # file on the removable medium is touched.
        os.replace(temp_name, descriptor_path)
        temp_name = None
        replaced = True

        if not verify_callback(root):
            try:
                _restore_descriptor(root, descriptor_path, original_bytes)
            except OSError as restore_exc:
                raise MediaCreatorError(
                    "WRITE VERIFICATION FAILED AND ORIGINAL METADATA RESTORE FAILED: "
                    f"{restore_exc}"
                ) from restore_exc
            raise MediaCreatorError("WRITE VERIFICATION FAILED; ORIGINAL METADATA RESTORED")

    except MediaCreatorError:
        raise
    except OSError as exc:
        if replaced:
            try:
                _restore_descriptor(root, descriptor_path, original_bytes)
            except OSError as restore_exc:
                raise MediaCreatorError(
                    f"MEDIA REPLACE FAILED: {exc}; ORIGINAL RESTORE FAILED: {restore_exc}"
                ) from restore_exc
        raise MediaCreatorError(f"MEDIA REPLACE FAILED: {exc}") from exc
    finally:
        if temp_name:
            try:
                Path(temp_name).unlink(missing_ok=True)
            except OSError:
                pass

    return root, descriptor_path


def replace_launch_key_on_target(game, target_path):
    """Explicitly replace an existing J-29 descriptor with a launch key."""
    fields = _launch_key_fields(game)
    descriptor_text = build_launch_key_descriptor(game)
    valid, status = validate_launch_key_descriptor(descriptor_text)
    if not valid:
        raise MediaCreatorError(status)

    root, descriptor_path = _replace_descriptor_atomically(
        descriptor_text,
        target_path,
        lambda volume: _verify_launch_key_write(volume, fields),
    )

    return {
        "success": True,
        "replaced": True,
        "target_path": str(root),
        "descriptor_path": str(descriptor_path),
        "title": fields["title"],
        "platform": fields["platform"],
        "game_id": fields["game_id"],
        "verified": True,
    }


def replace_collection_on_target(games, title, target_path):
    """Explicitly replace an existing J-29 descriptor with a collection."""
    ordered = _collection_games(games)
    collection_title = _clean(title) or "J-29 COLLECTION"
    descriptor_text = build_collection_descriptor(ordered, collection_title)
    valid, status = validate_collection_descriptor(descriptor_text)
    if not valid:
        raise MediaCreatorError(status)

    expected_ids = [_launch_key_fields(game)["game_id"] for game in ordered]
    root, descriptor_path = _replace_descriptor_atomically(
        descriptor_text,
        target_path,
        lambda volume: _verify_collection_write(volume, collection_title, expected_ids),
    )

    return {
        "success": True,
        "replaced": True,
        "target_path": str(root),
        "descriptor_path": str(descriptor_path),
        "title": collection_title,
        "item_count": len(expected_ids),
        "game_ids": expected_ids,
        "verified": True,
    }

