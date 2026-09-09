from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AuxPresentation:
    state: str
    line1: str
    line2: str
    priority: int
    persistent: bool
    timeout_ms: int | None = None


STATE_RULES = {
    "READY": {"priority": 10, "persistent": True, "line1": "J-29", "line2": "READY"},
    "BOOTING": {"priority": 80, "persistent": True, "line1": "J-29", "line2": "BOOTING"},
    "REBOOTING": {"priority": 90, "persistent": True, "line1": "J-29", "line2": "REBOOTING"},
    "MAINTENANCE": {"priority": 50, "persistent": True, "line1": "J-29", "line2": "MAINTENANCE"},
    "MEDIA_DETECTED": {"priority": 30, "persistent": False, "timeout_ms": 3000, "line1": "MEDIA DETECTED"},
    "GAME_LAUNCHING": {"priority": 60, "persistent": True, "line1": "GAME LAUNCHING"},
    "GAME_RUNNING": {"priority": 70, "persistent": True, "line1": "GAME RUNNING"},
    "LAUNCH_FAILED": {"priority": 75, "persistent": False, "timeout_ms": 2500, "line1": "LAUNCH FAILED"},
    "SHUTDOWN": {"priority": 100, "persistent": True, "line1": "J-29", "line2": "SHUTDOWN"},
    "CLEAR": {"priority": 0, "persistent": True, "line1": "", "line2": ""},
}


def _clean(value):
    return " ".join(str(value or "").strip().split())


def truncate_text(value, width=16):
    width = max(4, int(width))
    text = _clean(value)
    if len(text) <= width:
        return text
    return text[: width - 3].rstrip() + "..."


def build_presentation(state, line1="", line2="", width=16):
    state = _clean(state).upper() or "STATUS"
    rule = STATE_RULES.get(state, {"priority": 20, "persistent": True})

    resolved_line1 = _clean(line1) or rule.get("line1", state.replace("_", " "))
    resolved_line2 = _clean(line2) or rule.get("line2", "")

    return AuxPresentation(
        state=state,
        line1=truncate_text(resolved_line1, width),
        line2=truncate_text(resolved_line2, width),
        priority=int(rule.get("priority", 20)),
        persistent=bool(rule.get("persistent", True)),
        timeout_ms=rule.get("timeout_ms"),
    )
