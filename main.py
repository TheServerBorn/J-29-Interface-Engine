from engine.setup_state import is_first_launch_complete
from shells.terminal import terminal_ui


def run_first_launch_setup():
    print("=" * 50)
    print("VEYLLISTO FIRST-LAUNCH SETUP")
    print("Setup UI not implemented yet.")
    print("=" * 50)


def main():
    if not is_first_launch_complete():
        run_first_launch_setup()
        return

    terminal_ui.run()


if __name__ == "__main__":
    main()