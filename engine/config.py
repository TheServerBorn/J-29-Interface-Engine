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
    }