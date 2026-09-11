from engine.setup_state import (
    is_first_launch_complete,
    mark_first_launch_complete,
)
from setup.first_launch import run as run_first_launch


def run_terminal():
    from shells.terminal import terminal_ui
    terminal_ui.run()


def main():
    if not is_first_launch_complete():
        choice = run_first_launch()

        if choice == "beginner":
            print("Guided setup selected.")
            return

        if choice == "power_user_confirmed":
            mark_first_launch_complete()
            run_terminal()
            return

        return

    run_terminal()


if __name__ == "__main__":
    main()