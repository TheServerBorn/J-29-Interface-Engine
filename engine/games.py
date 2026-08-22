from engine.config import load_config


def load_games(config_path="games.ini"):
    config = load_config(config_path)

    games = []

    for section in config.sections():
        games.append({
            "name": config[section]["name"],
            "path": config[section]["path"]
        })

    return games