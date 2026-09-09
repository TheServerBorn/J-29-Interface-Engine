from __future__ import annotations

import configparser
import hashlib
import hmac
import os
from pathlib import Path


AUTH_FILE = Path("config/maintenance_auth.ini")
ALGORITHM = "pbkdf2_sha256"
DEFAULT_ITERATIONS = 310_000
SALT_BYTES = 16


def _read_auth(path=AUTH_FILE):
    path = Path(path)
    if not path.exists():
        return None

    config = configparser.ConfigParser()
    try:
        config.read(path, encoding="utf-8")
        section = config["MAINTENANCE_AUTH"]
        return {
            "algorithm": section.get("algorithm", ""),
            "iterations": section.getint("iterations"),
            "salt": section.get("salt", ""),
            "hash": section.get("hash", ""),
        }
    except (KeyError, ValueError, configparser.Error):
        return None


def is_configured(path=AUTH_FILE):
    data = _read_auth(path)
    if not data:
        return False
    return (
        data["algorithm"] == ALGORITHM
        and data["iterations"] > 0
        and bool(data["salt"])
        and bool(data["hash"])
    )


def _derive(password, salt, iterations):
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        iterations,
    )


def verify_password(password, path=AUTH_FILE):
    data = _read_auth(path)
    if not data or data["algorithm"] != ALGORITHM:
        return False

    try:
        salt = bytes.fromhex(data["salt"])
        expected = bytes.fromhex(data["hash"])
        actual = _derive(password, salt, data["iterations"])
    except (ValueError, TypeError):
        return False

    return hmac.compare_digest(actual, expected)


def set_password(password, path=AUTH_FILE, iterations=DEFAULT_ITERATIONS):
    password = str(password or "")
    if len(password) < 6:
        raise ValueError("Maintenance password must be at least 6 characters.")

    iterations = int(iterations)
    if iterations < 100_000:
        raise ValueError("PBKDF2 iteration count is too low.")

    salt = os.urandom(SALT_BYTES)
    digest = _derive(password, salt, iterations)

    config = configparser.ConfigParser()
    config["MAINTENANCE_AUTH"] = {
        "version": "1",
        "algorithm": ALGORITHM,
        "iterations": str(iterations),
        "salt": salt.hex(),
        "hash": digest.hex(),
    }

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    # Write atomically so a failed update cannot leave a half-written auth file.
    temp_path = path.with_suffix(path.suffix + ".tmp")
    with temp_path.open("w", encoding="utf-8") as handle:
        config.write(handle)
    temp_path.replace(path)

    return True
