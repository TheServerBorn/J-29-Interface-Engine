from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from getpass import getpass

from engine.maintenance_auth import set_password


def main():
    print("J-29 MAINTENANCE CREDENTIAL SETUP")
    print("--------------------------------")
    print("The password itself is never written to the configuration file.")
    print()

    first = getpass("New maintenance password: ")
    second = getpass("Confirm maintenance password: ")

    if first != second:
        raise SystemExit("Passwords do not match.")

    try:
        set_password(first)
    except ValueError as exc:
        raise SystemExit(str(exc))

    print("Maintenance credential configured successfully.")


if __name__ == "__main__":
    main()
