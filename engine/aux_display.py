from __future__ import annotations

import json
import threading
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from engine.aux_presentation import build_presentation


@dataclass(frozen=True)
class AuxDisplayMessage:
    state: str
    line1: str = ""
    line2: str = ""


class AuxDisplayAdapter:
    """Hardware/backend interface for a secondary status display."""

    def show(self, message: AuxDisplayMessage):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def close(self):
        pass


class NullAuxDisplayAdapter(AuxDisplayAdapter):
    def show(self, message: AuxDisplayMessage):
        return False

    def clear(self):
        return False


class DebugFileAuxDisplayAdapter(AuxDisplayAdapter):
    """
    Development adapter for v0.30.0.

    Writes the latest display state to a JSON file. This lets the engine and
    shell integration be tested before any physical OLED library or device is
    selected.
    """

    def __init__(self, path="config/aux_display_debug.json"):
        self.path = Path(path)

    def show(self, message: AuxDisplayMessage):
        payload = {
            "state": message.state,
            "line1": message.line1,
            "line2": message.line2,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }

        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            temp_path = self.path.with_suffix(self.path.suffix + ".tmp")
            temp_path.write_text(
                json.dumps(payload, indent=2) + "\n",
                encoding="utf-8",
            )
            temp_path.replace(self.path)
            return True
        except OSError:
            return False

    def clear(self):
        return self.show(AuxDisplayMessage("CLEAR", "", ""))


class AuxiliaryDisplayManager:
    def __init__(self, settings=None):
        self.enabled = False
        self.adapter_name = "none"
        self.display_width = 16
        self._adapter: AuxDisplayAdapter = NullAuxDisplayAdapter()
        self._last_message = AuxDisplayMessage("OFFLINE", "", "")
        self._current_priority = 0
        self._persistent_message = AuxDisplayMessage("READY", "J-29", "READY")
        self._persistent_priority = 10
        self._timer = None
        self._lock = threading.RLock()
        self.configure(settings or {})

    def configure(self, settings):
        with self._lock:
            if self._timer is not None:
                self._timer.cancel()
                self._timer = None

            try:
                self._adapter.close()
            except Exception:
                pass

            self.enabled = bool(settings.get("aux_display_enabled", False))
            self.adapter_name = str(settings.get("aux_display_adapter", "debug")).strip().lower()
            self.display_width = max(8, int(settings.get("aux_display_width", 16)))

            if not self.enabled:
                self._adapter = NullAuxDisplayAdapter()
                return

            if self.adapter_name == "debug":
                self._adapter = DebugFileAuxDisplayAdapter(
                    settings.get("aux_display_debug_file", "config/aux_display_debug.json")
                )
            else:
                self._adapter = NullAuxDisplayAdapter()

    def _emit(self, message, priority):
        self._last_message = message
        self._current_priority = priority
        if not self.enabled:
            return False
        try:
            return bool(self._adapter.show(message))
        except Exception:
            return False

    def _restore_persistent(self):
        with self._lock:
            self._timer = None
            self._emit(self._persistent_message, self._persistent_priority)

    def _transition_allowed(self, next_state, next_priority, force):
        if force:
            return True

        current_state = self._last_message.state

        # SHUTDOWN is terminal for the current app session. Only a new BOOTING
        # state (new process/session) or an explicit force may replace it.
        if current_state == "SHUTDOWN":
            return next_state == "BOOTING"

        # READY is a legitimate lifecycle completion state after boot, reboot,
        # maintenance, launch failure, or a running game. It is not a generic
        # priority bypass.
        if next_state == "READY":
            return current_state in {
                "OFFLINE",
                "READY",
                "BOOTING",
                "REBOOTING",
                "MAINTENANCE",
                "GAME_LAUNCHING",
                "GAME_RUNNING",
                "LAUNCH_FAILED",
                "MEDIA_DETECTED",
            }

        return next_priority >= self._current_priority

    def show(self, state, line1="", line2="", force=False):
        presentation = build_presentation(state, line1, line2, width=self.display_width)
        message = AuxDisplayMessage(
            presentation.state,
            presentation.line1,
            presentation.line2,
        )

        with self._lock:
            if not self._transition_allowed(
                presentation.state,
                presentation.priority,
                force,
            ):
                return False

            if self._timer is not None:
                self._timer.cancel()
                self._timer = None

            if presentation.persistent:
                self._persistent_message = message
                self._persistent_priority = presentation.priority

            result = self._emit(message, presentation.priority)

            if not presentation.persistent and presentation.timeout_ms:
                self._timer = threading.Timer(
                    presentation.timeout_ms / 1000.0,
                    self._restore_persistent,
                )
                self._timer.daemon = True
                self._timer.start()

            return result

    def clear(self):
        with self._lock:
            if self._timer is not None:
                self._timer.cancel()
                self._timer = None

            message = AuxDisplayMessage("CLEAR", "", "")
            self._persistent_message = message
            self._persistent_priority = 0
            return self._emit(message, 0)

    def get_last_message(self):
        return self._last_message

    def close(self):
        with self._lock:
            if self._timer is not None:
                self._timer.cancel()
                self._timer = None
            try:
                self._adapter.close()
            except Exception:
                pass

