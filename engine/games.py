import configparser


def load_games(config_path="games.ini"):
    config = configparser.ConfigParser()
    config.read(config_path)

    games = []

    for section in config.sections():
        games.append({
            "name": config[section]["name"],
            "path": config[section]["path"]
        })

    return games