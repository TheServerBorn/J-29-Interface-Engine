from engine.config import load_config


DEFAULT_LIBRARY_FOLDER = "PROGRAMS"


def load_games(config_path="config/games.ini"):
    config = load_config(config_path)

    games = []

    for section in config.sections():

        name = config[section].get(
            "name",
            section
        ).strip()

        path = config[section].get(
            "path",
            ""
        ).strip()

        folder = config[section].get(
            "folder",
            DEFAULT_LIBRARY_FOLDER
        ).strip()

        if not folder:
            folder = DEFAULT_LIBRARY_FOLDER

        games.append({
            "name": name,
            "path": path,
            "folder": folder.upper()
        })

    return games