from pathlib import Path

from engine.library import build_library
from engine.audio import AudioManager
from engine.aux_display import AuxiliaryDisplayManager
from engine.theme import load_theme
from engine.games import load_games
from engine.steam import discover_steam_games
from engine.roms import discover_rom_games
from engine.game_state import load_game_state, save_game_state
from engine.launcher import launch_program_with_handle, launch_steam_app
from engine.emulators import launch_rom_with_handle
from engine.config import load_identity, load_settings
from engine.media import MediaMonitor, inspect_media
from engine.media_creator import (
    eligible_launch_key_games,
    preview_launch_key,
    preview_collection,
    list_safe_media_targets,
    write_launch_key_to_target,
    write_collection_to_target,
    inspect_existing_media,
    replace_launch_key_on_target,
    replace_collection_on_target,
)
from engine.system_info import (
    get_cpu_name,
    get_memory_gb,
    get_storage_info,
    get_os_name,
)


class J29Engine:
    def __init__(self):
        self._last_launch_error = ""
        self._last_launch_process = None
        self._last_launch_type = ""
        self._media_monitor = MediaMonitor()

        settings = load_settings()
        theme = load_theme(
            f"themes/{settings['theme']}/theme.ini"
        )
        self._audio = AudioManager(settings=settings, theme=theme)
        self._aux_display = AuxiliaryDisplayManager(settings=settings)

    def get_last_launch_error(self):
        return self._last_launch_error

    def get_last_launch_process(self):
        return self._last_launch_process

    def get_last_launch_type(self):
        return self._last_launch_type

    def play_sound(self, event_name):
        return self._audio.play(event_name)

    def stop_audio(self):
        self._audio.stop()

    def reload_audio(self):
        settings = load_settings()
        theme = load_theme(
            f"themes/{settings['theme']}/theme.ini"
        )
        self._audio.configure(settings=settings, theme=theme)


    def set_aux_display(self, state, line1="", line2=""):
        return self._aux_display.show(state, line1, line2)

    def clear_aux_display(self):
        return self._aux_display.clear()

    def get_aux_display_state(self):
        return self._aux_display.get_last_message()

    def get_aux_display_status(self):
        return self._aux_display.get_adapter_status()

    def test_aux_display(self):
        """Send a temporary, recognizable auxiliary-display test."""
        return self._aux_display.show(
            "DISPLAY_TEST",
            "J-29",
            "DISPLAY TEST",
            force=True,
        )

    def reload_aux_display(self):
        self._aux_display.configure(load_settings())

    def close_aux_display(self):
        self._aux_display.close()


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
        self._last_launch_process = None
        self._last_launch_type = ""

        if not game:
            self._last_launch_error = "PROGRAM RECORD NOT AVAILABLE"
            self.set_aux_display("LAUNCH_FAILED", "LAUNCH FAILED", "PROGRAM")
            return False

        title = str(
            game.get("title")
            or game.get("name")
            or game.get("id")
            or "PROGRAM"
        ).strip()
        launch_type = str(game.get("launch_type", "EXECUTABLE")).upper()

        if launch_type == "LIBRARY":
            target_game_id = str(game.get("target_game_id", "")).strip()
            target = next(
                (
                    candidate
                    for candidate in self.get_games()
                    if str(candidate.get("id", "")).strip() == target_game_id
                ),
                None,
            )
            if not target:
                self._last_launch_error = (
                    f"LIBRARY GAME NOT FOUND: {target_game_id}"
                    if target_game_id
                    else "LIBRARY GAME ID NOT PROVIDED"
                )
                self.set_aux_display("LAUNCH_FAILED", "LAUNCH FAILED", title[:32])
                return False
            return self.launch_game(target)

        self._last_launch_type = launch_type
        self.set_aux_display("GAME_LAUNCHING", "LAUNCHING", title[:32])

        if launch_type == "STEAM":
            launched = launch_steam_app(game.get("steam_id"))
            if not launched:
                self._last_launch_error = "STEAM LAUNCH FAILED"
        elif launch_type == "EXECUTABLE":
            launched, process = launch_program_with_handle(
                game.get("executable_path") or game.get("path")
            )
            self._last_launch_process = process
            if not launched:
                self._last_launch_error = "PROGRAM NOT AVAILABLE"
        elif launch_type == "ROM":
            launched, detail, process = launch_rom_with_handle(game)
            self._last_launch_process = process
            if not launched:
                self._last_launch_error = detail
        else:
            launched = False
            self._last_launch_error = f"UNSUPPORTED LAUNCH TYPE: {launch_type}"

        if launched:
            # Keep GAME_LAUNCHING visible long enough for the shell/display
            # layer to present it intentionally. The Terminal Shell promotes
            # the session to GAME_RUNNING after a short non-blocking delay.
            if game.get("id"):
                self.record_recent_game(game["id"])
        else:
            self.set_aux_display("LAUNCH_FAILED", "LAUNCH FAILED", title[:32])

        return launched

    def get_media_creator_games(self):
        return eligible_launch_key_games(self.get_games())

    def preview_media_launch_key(self, game):
        return preview_launch_key(game)

    def preview_media_collection(self, games, title):
        return preview_collection(games, title)

    def get_media_creator_targets(self):
        return list_safe_media_targets()

    def write_media_launch_key(self, game, target_path):
        return write_launch_key_to_target(game, target_path)

    def write_media_collection(self, games, title, target_path):
        return write_collection_to_target(games, title, target_path)

    def get_existing_media_summary(self, target_path):
        return inspect_existing_media(target_path)

    def replace_media_launch_key(self, game, target_path):
        return replace_launch_key_on_target(game, target_path)

    def replace_media_collection(self, games, title, target_path):
        return replace_collection_on_target(games, title, target_path)

    def get_present_media(self):
        return self._media_monitor.present()

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