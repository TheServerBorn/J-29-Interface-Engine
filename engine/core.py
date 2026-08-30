from pathlib import Path

from engine.library import build_library
from engine.theme import load_theme
from engine.games import load_games
from engine.steam import discover_steam_games
from engine.roms import discover_rom_games
from engine.game_state import load_game_state, save_game_state
from engine.launcher import launch_program, launch_steam_app
from engine.emulators import launch_rom_with_status
from engine.config import load_identity, load_settings
from engine.media import MediaMonitor, inspect_media
from engine.system_info import (
    get_cpu_name,
    get_memory_gb,
    get_storage_info,
    get_os_name,
)


class J29Engine:
    def __init__(self):
        self._last_launch_error = ""
        self._media_monitor = MediaMonitor()

    def get_last_launch_error(self):
        return self._last_launch_error

    def get_games(self):
        configured_games = load_games()
        steam_games = discover_steam_games()
        rom_games = discover_rom_games()

        # Manually configured integration records win over discovery so users
        # can add richer metadata without creating duplicate library entries.
        configured_steam_ids = {
            str(game.get("steam_id", "")).strip()
            for game in configured_games
            if game.get("steam_id")
        }

        def normalized_path(value):
            try:
                return str(Path(str(value)).expanduser().resolve()).casefold()
            except (OSError, TypeError, ValueError):
                return str(value or "").strip().casefold()

        configured_rom_paths = {
            normalized_path(game.get("rom_path") or game.get("path"))
            for game in configured_games
            if str(game.get("launch_type", "")).upper() == "ROM"
            and (game.get("rom_path") or game.get("path"))
        }

        auto_steam_games = [
            game
            for game in steam_games
            if game.get("steam_id") not in configured_steam_ids
        ]

        auto_rom_games = [
            game
            for game in rom_games
            if normalized_path(game.get("rom_path") or game.get("path"))
            not in configured_rom_paths
        ]

        return configured_games + auto_steam_games + auto_rom_games
    
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
        self._last_launch_error = ""

        if not game:
            self._last_launch_error = "PROGRAM RECORD NOT AVAILABLE"
            return False

        launch_type = str(game.get("launch_type", "EXECUTABLE")).upper()

        if launch_type == "STEAM":
            launched = launch_steam_app(game.get("steam_id"))
            if not launched:
                self._last_launch_error = "STEAM LAUNCH FAILED"
        elif launch_type == "EXECUTABLE":
            launched = launch_program(
                game.get("executable_path") or game.get("path")
            )
            if not launched:
                self._last_launch_error = "PROGRAM NOT AVAILABLE"
        elif launch_type == "ROM":
            launched, detail = launch_rom_with_status(game)
            if not launched:
                self._last_launch_error = detail
        else:
            launched = False
            self._last_launch_error = f"UNSUPPORTED LAUNCH TYPE: {launch_type}"

        if launched and game.get("id"):
            self.record_recent_game(game["id"])

        return launched

    def poll_media_events(self):
        return self._media_monitor.poll()

    def poll_inserted_media(self):
        # Backward-compatible helper for the initial v0.26 shell checkpoint.
        return self.poll_media_events()["inserted"]

    def inspect_media(self, volume):
        return inspect_media(volume)

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