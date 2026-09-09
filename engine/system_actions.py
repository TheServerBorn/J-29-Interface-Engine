from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def restart_application():
    """
    Replace the current J-29 process with a fresh process.

    This is intentionally different from the in-app REBOOT command, which only
    reruns the fictional boot sequence inside the existing Python process.
    """
    if getattr(sys, "frozen", False):
        executable = sys.executable
        args = [executable, *sys.argv[1:]]
    else:
        executable = sys.executable
        script = Path(sys.argv[0]).resolve()
        args = [executable, str(script), *sys.argv[1:]]

    os.execv(executable, args)


def _host_command(action):
    if os.name == "nt":
        if action == "reboot":
            return ["shutdown", "/r", "/t", "0"]
        if action == "shutdown":
            return ["shutdown", "/s", "/t", "0"]

    if sys.platform == "darwin":
        if action == "reboot":
            return ["shutdown", "-r", "now"]
        if action == "shutdown":
            return ["shutdown", "-h", "now"]

    # Linux / other Unix-like systems.
    if action == "reboot":
        return ["shutdown", "-r", "now"]
    if action == "shutdown":
        return ["shutdown", "-h", "now"]

    raise ValueError(f"Unsupported host action: {action}")


def request_host_action(action):
    """
    Request a host reboot or shutdown.

    Returns True if the OS command was successfully started. Permission/policy
    failures are surfaced to the caller as exceptions.
    """
    command = _host_command(str(action or "").strip().lower())
    subprocess.Popen(command)
    return True
