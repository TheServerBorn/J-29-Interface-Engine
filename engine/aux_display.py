from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


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
    """
    Engine-level semantic auxiliary-display service.

    Shells report machine state. Adapters decide how that state reaches actual
    hardware. Failures are intentionally nonfatal; the primary J-29 interface
    must never depend on an auxiliary display being present.
    """

    def __init__(self, settings=None):
        self.enabled = False
        self.adapter_name = "none"
        self._adapter: AuxDisplayAdapter = NullAuxDisplayAdapter()
        self._last_message = AuxDisplayMessage("OFFLINE", "", "")
        self.configure(settings or {})

    def configure(self, settings):
        try:
            self._adapter.close()
        except Exception:
            pass

        self.enabled = bool(settings.get("aux_display_enabled", False))
        self.adapter_name = str(
            settings.get("aux_display_adapter", "debug")
        ).strip().lower()

        if not self.enabled:
            self._adapter = NullAuxDisplayAdapter()
            return

        if self.adapter_name == "debug":
            self._adapter = DebugFileAuxDisplayAdapter(
                settings.get(
                    "aux_display_debug_file",
                    "config/aux_display_debug.json",
                )
            )
        else:
            # Unknown hardware adapters fail closed/silent until explicitly
            # implemented in a later v0.30 slice.
            self._adapter = NullAuxDisplayAdapter()

    def show(self, state, line1="", line2=""):
        message = AuxDisplayMessage(
            state=str(state or "STATUS").strip().upper(),
            line1=str(line1 or "").strip(),
            line2=str(line2 or "").strip(),
        )
        self._last_message = message

        if not self.enabled:
            return False

        try:
            return bool(self._adapter.show(message))
        except Exception:
            return False

    def clear(self):
        self._last_message = AuxDisplayMessage("CLEAR", "", "")
        if not self.enabled:
            return False
        try:
            return bool(self._adapter.clear())
        except Exception:
            return False

    def get_last_message(self):
        return self._last_message

    def close(self):
        try:
            self._adapter.close()
        except Exception:
            pass
