from __future__ import annotations

import json
import threading
import time

try:
    import serial
except ImportError:  # Optional dependency for physical hardware.
    serial = None
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

    def connect(self):
        return True

    def disconnect(self):
        return True

    def is_available(self):
        return True

    def get_last_error(self):
        return ""

    def show(self, message: AuxDisplayMessage):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def close(self):
        self.disconnect()


class NullAuxDisplayAdapter(AuxDisplayAdapter):
    def __init__(self, reason=""):
        self._reason = str(reason or "")

    def connect(self):
        return False

    def disconnect(self):
        return True

    def is_available(self):
        return False

    def get_last_error(self):
        return self._reason

    def show(self, message: AuxDisplayMessage):
        return False

    def clear(self):
        return False


class DebugFileAuxDisplayAdapter(AuxDisplayAdapter):
    """
    Development adapter. Writes the latest rendered state to JSON.
    """

    def __init__(self, path="config/aux_display_debug.json"):
        self.path = Path(path)
        self._last_error = ""

    def connect(self):
        self._last_error = ""
        return True

    def disconnect(self):
        return True

    def is_available(self):
        return True

    def get_last_error(self):
        return self._last_error

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
            self._last_error = ""
            return True
        except OSError as exc:
            self._last_error = str(exc)
            return False

    def clear(self):
        return self.show(AuxDisplayMessage("CLEAR", "", ""))


class SerialAuxDisplayAdapter(AuxDisplayAdapter):
    """
    First physical-display transport for J-29.

    This adapter talks to a USB/serial display bridge (for example a small
    microcontroller that drives an OLED). J-29 sends one compact UTF-8 line
    per rendered update:

        J29|<STATE>|<LINE1>|<LINE2>\n

    The bridge decides how those final lines are drawn on the attached display.
    """

    def __init__(
        self,
        port,
        baudrate=115200,
        reconnect_seconds=2.0,
        timeout=0.25,
    ):
        self.port = str(port or "").strip()
        self.baudrate = int(baudrate)
        self.reconnect_seconds = max(0.25, float(reconnect_seconds))
        self.timeout = max(0.05, float(timeout))
        self._serial = None
        self._last_error = ""
        self._last_connect_attempt = 0.0
        self._lock = threading.RLock()

    def _sanitize(self, value):
        return (
            str(value or "")
            .replace("|", "/")
            .replace("\r", " ")
            .replace("\n", " ")
            .strip()
        )

    def _packet(self, message):
        return (
            "J29|"
            + self._sanitize(message.state)
            + "|"
            + self._sanitize(message.line1)
            + "|"
            + self._sanitize(message.line2)
            + "\n"
        ).encode("utf-8")

    def connect(self):
        with self._lock:
            if self.is_available():
                return True

            now = time.monotonic()
            if now - self._last_connect_attempt < self.reconnect_seconds:
                return False
            self._last_connect_attempt = now

            if serial is None:
                self._last_error = (
                    "PYSERIAL NOT INSTALLED — RUN: pip install pyserial"
                )
                return False

            if not self.port:
                self._last_error = "SERIAL PORT NOT CONFIGURED"
                return False

            try:
                self._serial = serial.Serial(
                    port=self.port,
                    baudrate=self.baudrate,
                    timeout=self.timeout,
                    write_timeout=self.timeout,
                )
                self._last_error = ""
                return True
            except Exception as exc:
                self._serial = None
                self._last_error = str(exc)
                return False

    def disconnect(self):
        with self._lock:
            try:
                if self._serial is not None:
                    self._serial.close()
            except Exception:
                pass
            self._serial = None
            return True

    def is_available(self):
        try:
            return bool(
                self._serial is not None
                and getattr(self._serial, "is_open", False)
            )
        except Exception:
            return False

    def get_last_error(self):
        return self._last_error

    def show(self, message: AuxDisplayMessage):
        with self._lock:
            if not self.is_available() and not self.connect():
                return False

            try:
                self._serial.write(self._packet(message))
                self._serial.flush()
                self._last_error = ""
                return True
            except Exception as exc:
                self._last_error = str(exc)
                self.disconnect()
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
                self._adapter = NullAuxDisplayAdapter("AUXILIARY DISPLAY DISABLED")
                return

            if self.adapter_name == "debug":
                self._adapter = DebugFileAuxDisplayAdapter(
                    settings.get("aux_display_debug_file", "config/aux_display_debug.json")
                )
            elif self.adapter_name == "serial":
                self._adapter = SerialAuxDisplayAdapter(
                    port=settings.get("aux_display_serial_port", ""),
                    baudrate=settings.get("aux_display_serial_baudrate", 115200),
                    reconnect_seconds=settings.get(
                        "aux_display_reconnect_seconds",
                        2.0,
                    ),
                )
            else:
                self._adapter = NullAuxDisplayAdapter(
                    f"UNSUPPORTED AUX DISPLAY ADAPTER: {self.adapter_name}"
                )

            # Physical hardware may not be connected yet. Connection failure is
            # intentionally nonfatal; show() will retry on future updates.
            self._adapter.connect()

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

    def is_available(self):
        try:
            return bool(self._adapter.is_available())
        except Exception:
            return False

    def get_adapter_status(self):
        return {
            "enabled": self.enabled,
            "adapter": self.adapter_name,
            "available": self.is_available(),
            "error": self.get_last_error(),
        }

    def get_last_error(self):
        try:
            return str(self._adapter.get_last_error() or "")
        except Exception:
            return "AUXILIARY DISPLAY STATUS UNAVAILABLE"

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

