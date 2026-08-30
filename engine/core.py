from engine.library import build_library
from engine.theme import load_theme
from engine.games import load_games
from engine.steam import discover_steam_games
from engine.game_state import load_game_state, save_game_state
from engine.launcher import launch_program, launch_steam_app
from engine.config import load_identity, load_settings
from engine.system_info import (
    get_cpu_name,
    get_memory_gb,
    get_storage_info,
    get_os_name,
)


class J29Engine:
    def get_games(self):
        configured_games = load_games()
        steam_games = discover_steam_games()

        # A manually configured Steam entry wins over auto-discovery so users
        # can supply richer metadata without seeing a duplicate title.
        configured_steam_ids = {
            str(game.get("steam_id", "")).strip()
            for game in configured_games
            if game.get("steam_id")
        }

        auto_games = [
            game
            for game in steam_games
            if game.get("steam_id") not in configured_steam_ids
        ]

        return configured_games + auto_games
    
    def get_library(self):
        return build_library(
            self.get_games()
        )

    def get_favorite_games(self):
        favorite_ids = set(load_game_state().get("favorites", []))

        return [
            game
            for game in self.get_games()
            if game["id"] in favorite_ids
        ]

    def is_favorite(self, game_id):
        favorites = load_game_state().get("favorites", [])
        return game_id in favorites

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
    
    def get_recent_games(self):
        recent_ids = load_game_state().get("recent", [])
        games_by_id = {game["id"]: game for game in self.get_games()}

        return [
            games_by_id[game_id]
            for game_id in recent_ids
            if game_id in games_by_id
        ]

    def record_recent_game(self, game_id):
        state = load_game_state()
        recent = state.get("recent", [])

        if game_id in recent:
            recent.remove(game_id)

        recent.insert(0, game_id)
        state["recent"] = recent
        save_game_state(state)

    def launch_game(self, game):
        if not game:
            return False

        launch_type = str(game.get("launch_type", "EXECUTABLE")).upper()

        if launch_type == "STEAM":
            launched = launch_steam_app(game.get("steam_id"))
        elif launch_type == "EXECUTABLE":
            launched = launch_program(
                game.get("executable_path") or game.get("path")
            )
        else:
            # ROM/emulator dispatch belongs to v0.25. Unknown launch types
            # fail safely instead of leaking platform logic into the shell.
            launched = False

        if launched and game.get("id"):
            self.record_recent_game(game["id"])

        return launched

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