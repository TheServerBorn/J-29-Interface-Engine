import configparser


def load_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def load_identity(config_path="config/identity.ini"):
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