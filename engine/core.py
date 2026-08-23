from engine.theme import load_theme
from engine.games import load_games
from engine.game_state import load_game_state, save_game_state
from engine.launcher import launch_program
from engine.config import load_identity, load_settings
from engine.system_info import (
    get_cpu_name,
    get_memory_gb,
    get_storage_info,
    get_os_name,
)


class J29Engine:
    def get_games(self):
        return load_games()

    def get_favorite_games(self):
        state = load_game_state()
        favorite_ids = state.get("favorites", [])

        return [
            game
            for game in self.get_games()
            if game["id"] in favorite_ids
        ]

    def toggle_favorite(self, game_id):
        state = load_game_state()
        favorites = state.get("favorites", [])

        if game_id in favorites:
            favorites.remove(game_id)
            is_favorite = False
        else:
            favorites.append(game_id)
            is_favorite = True

        state["favorites"] = favorites
        save_game_state(state)

        return is_favorite

    def launch_game(self, program_path):
        return launch_program(program_path)

    def get_system_info(self):
        storage = get_storage_info()

        return {
            "cpu": get_cpu_name(),
            "memory_gb": get_memory_gb(),
            "os_name": get_os_name(),
            "system_drive": storage["system_drive"],
            "total_gb": storage["total_gb"],
            "free_gb": storage["free_gb"],
        }

    def get_identity(self):
        return load_identity()

    def get_settings(self):
        return load_settings()

    def get_theme(self):
        settings = load_settings()
        theme_name = settings["theme"]

        return load_theme(
            f"themes/{theme_name}/theme.ini"
        )