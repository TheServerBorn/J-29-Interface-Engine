from engine.config import load_settings, update_setting


def is_first_launch_complete():
    settings = load_settings()
    return settings.get("first_launch_complete", False)


def mark_first_launch_complete():
    update_setting(
        "SETUP",
        "first_launch_complete",
        "true"
    )


def reset_first_launch():
    update_setting(
        "SETUP",
        "first_launch_complete",
        "false"
    )