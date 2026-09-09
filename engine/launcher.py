"""Cross-platform launch helpers for J-29."""

import os
import platform
import shutil
import subprocess
import webbrowser


def launch_program_with_handle(program_path):
    """Launch an executable and preserve its process handle for lifecycle tracking."""
    if not program_path:
        return False, None

    try:
        process = subprocess.Popen([program_path])
        return True, process
    except (OSError, ValueError):
        return False, None


def launch_program(program_path):
    """Backward-compatible boolean executable launch helper."""
    launched, _process = launch_program_with_handle(program_path)
    return launched

def launch_uri(uri):
    """Open an OS-registered URI such as steam:// on any supported platform."""
    if not uri:
        return False

    system = platform.system()

    try:
        if system == "Windows":
            os.startfile(uri)  # type: ignore[attr-defined]
            return True

        if system == "Darwin":
            subprocess.Popen(["open", uri])
            return True

        opener = shutil.which("xdg-open")
        if opener:
            subprocess.Popen([opener, uri])
            return True

        # Last-resort fallback for uncommon Unix desktop environments.
        return bool(webbrowser.open(uri))

    except (OSError, ValueError):
        return False


def launch_steam_app(app_id):
    app_id = str(app_id or "").strip()

    if not app_id or not app_id.isdigit():
        return False

    return launch_uri(f"steam://run/{app_id}")
