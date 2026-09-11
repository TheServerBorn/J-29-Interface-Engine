import configparser
import shutil
from pathlib import Path


def load_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config

def ensure_config_file(config_path):
    config_file = Path(config_path)

    if config_file.exists():
        return

    template_file = config_file.with_name(
        f"{config_file.stem}.example{config_file.suffix}"
    )

    if template_file.exists():
        shutil.copyfile(template_file, config_file)

def load_identity(config_path="config/identity.ini"):
    ensure_config_file(config_path)
    config = load_config(config_path)

    return {
        "manufacturer": config.get(
            "SYSTEM",
            "manufacturer",
            fallback="Callisto Computer Systems"
        ),
        "os_name": config.get(
            "SYSTEM",
            "os_name",
            fallback="J-29 Terminal OS"
        ),
        "model": config.get(
            "SYSTEM",
            "model",
            fallback="J-29 Personal Terminal"
        ),
        "version": config.get(
            "SYSTEM",
            "version",
            fallback="0.15"
        ),
        "unit_id": config.get(
            "SYSTEM",
            "unit_id",
            fallback="J29-001"
        ),
        "owner": config.get(
            "OWNER",
            "name",
            fallback=""
        ),
        "location": config.get(
            "OWNER",
            "location",
            fallback=""
        ),
    }


def load_settings(config_path="config/settings.ini"):
    ensure_config_file(config_path)
    config = load_config(config_path)

    return {
        "fullscreen": config.getboolean(
            "INTERFACE",
            "fullscreen",
            fallback=True
        ),
        "boot_sequence": config.getboolean(
            "INTERFACE",
            "boot_sequence",
            fallback=True
        ),
        "show_footer": config.getboolean(
            "INTERFACE",
            "show_footer",
            fallback=True
        ),
        "theme": config.get(
            "INTERFACE",
            "theme",
            fallback="callisto_green"
        ),
        "audio_enabled": config.getboolean(
            "AUDIO",
            "enabled",
            fallback=True
        ),
        "master_volume": config.getint(
            "AUDIO",
            "master_volume",
            fallback=70
        ),
        "aux_display_enabled": config.getboolean(
            "AUXILIARY_DISPLAY",
            "enabled",
            fallback=False
        ),
        "aux_display_adapter": config.get(
            "AUXILIARY_DISPLAY",
            "adapter",
            fallback="debug"
        ),
        "aux_display_debug_file": config.get(
            "AUXILIARY_DISPLAY",
            "debug_file",
            fallback="config/aux_display_debug.json"
        ),
        "aux_display_width": config.getint(
            "AUXILIARY_DISPLAY",
            "width",
            fallback=16
        ),
        "aux_display_serial_port": config.get(
            "AUXILIARY_DISPLAY",
            "serial_port",
            fallback=""
        ),
        "aux_display_serial_baudrate": config.getint(
            "AUXILIARY_DISPLAY",
            "serial_baudrate",
            fallback=115200
        ),
        "aux_display_reconnect_seconds": config.getfloat(
            "AUXILIARY_DISPLAY",
            "reconnect_seconds",
            fallback=2.0
        ),
        "fullscreen_key": config.get(
            "DEVELOPMENT",
            "fullscreen_key",
            fallback="F11"
        ),
        "windowed_key": config.get(
            "DEVELOPMENT",
            "windowed_key",
            fallback="F12"
        ),
        "first_launch_complete": config.getboolean(
            "SETUP",
            "first_launch_complete",
            fallback=False,
        ),
    }

def update_setting(
    section,
    key,
    value,
    config_path="config/settings.ini",
):
    """
    Atomically update a single setting while preserving all other
    sections and values.
    """
    ensure_config_file(config_path)
    path = Path(config_path)

    config = configparser.ConfigParser()
    config.read(path, encoding="utf-8")

    if not config.has_section(section):
        config.add_section(section)

    config.set(section, key, str(value))

    temp_path = path.with_suffix(path.suffix + ".tmp")

    try:
        with temp_path.open("w", encoding="utf-8") as handle:
            config.write(handle)

        temp_path.replace(path)

    except Exception:
        try:
            temp_path.unlink(missing_ok=True)
        except Exception:
            pass

        raise

MAINTENANCE_SETTING_MAP = {
    "fullscreen": ("INTERFACE", "fullscreen", "bool"),
    "theme": ("INTERFACE", "theme", "str"),
    "show_footer": ("INTERFACE", "show_footer", "bool"),
    "aux_display_enabled": ("AUXILIARY_DISPLAY", "enabled", "bool"),
    "aux_display_adapter": ("AUXILIARY_DISPLAY", "adapter", "adapter"),
    "aux_display_width": ("AUXILIARY_DISPLAY", "width", "width"),
}


def list_available_themes(themes_root="themes"):
    root = Path(themes_root)
    if not root.exists():
        return []

    themes = []
    for child in root.iterdir():
        if child.is_dir() and (child / "theme.ini").exists():
            themes.append(child.name)

    return sorted(themes, key=str.casefold)


def _normalize_maintenance_setting(name, value, themes_root="themes"):
    if name not in MAINTENANCE_SETTING_MAP:
        raise ValueError(f"Unsupported maintenance setting: {name}")

    _section, _key, kind = MAINTENANCE_SETTING_MAP[name]

    if kind == "bool":
        return bool(value)

    if kind == "str":
        value = str(value or "").strip()
        if not value:
            raise ValueError(f"{name} cannot be empty.")

        if name == "theme":
            available = list_available_themes(themes_root)
            # If themes are available, require an exact existing theme.
            if available and value not in available:
                raise ValueError(f"Unknown theme: {value}")

        return value

    if kind == "adapter":
        value = str(value or "").strip().lower()
        if value not in ("debug", "serial"):
            raise ValueError("Aux adapter must be debug or serial.")
        return value

    if kind == "width":
        value = int(value)
        if value < 8 or value > 64:
            raise ValueError("Aux display width must be between 8 and 64.")
        return value

    raise ValueError(f"Unsupported setting type: {kind}")


def save_maintenance_settings(
    values,
    config_path="config/settings.ini",
    themes_root="themes",
):
    """
    Atomically save the maintenance editor's low-risk allowlisted settings.

    Existing unrelated settings/sections are preserved. If validation or the
    write fails, the original settings.ini remains untouched.
    """
    if not isinstance(values, dict):
        raise ValueError("Settings payload must be a dictionary.")

    normalized = {}
    for name, value in values.items():
        normalized[name] = _normalize_maintenance_setting(
            name,
            value,
            themes_root=themes_root,
        )

    ensure_config_file(config_path)
    path = Path(config_path)

    config = configparser.ConfigParser()
    config.read(path, encoding="utf-8")

    for name, value in normalized.items():
        section, key, kind = MAINTENANCE_SETTING_MAP[name]
        if not config.has_section(section):
            config.add_section(section)

        if kind == "bool":
            serialized = "true" if value else "false"
        else:
            serialized = str(value)

        config.set(section, key, serialized)

    temp_path = path.with_suffix(path.suffix + ".tmp")
    try:
        with temp_path.open("w", encoding="utf-8") as handle:
            config.write(handle)
        temp_path.replace(path)
    except Exception:
        try:
            temp_path.unlink(missing_ok=True)
        except Exception:
            pass
        raise

    return normalized
