from tkinter import Tk, Canvas


WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600

BACKGROUND = "#080B0F"
PRIMARY = "#E8EDF2"
SECONDARY = "#7F8C98"
ACCENT = "#9FB6C8"

TITLE_FONT = ("Courier New", 30, "bold")
SUBTITLE_FONT = ("Courier New", 13)
MENU_FONT = ("Courier New", 18)
INFO_FONT = ("Courier New", 11)

OPTIONS = [
    ("BEGINNER", "Guided system configuration"),
    ("POWER USER", "Skip guided setup and use system defaults"),
]


def run():
    root = Tk()

    root.title("Veyllisto Setup")
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.configure(bg=BACKGROUND)

    canvas = Canvas(
        root,
        bg=BACKGROUND,
        highlightthickness=0,
    )
    canvas.pack(fill="both", expand=True)

    selected = 0
    result = None
    current_screen = "welcome"

    def clear_screen():
        canvas.delete("all")

    def draw_header(subtitle):
        canvas.create_text(
            60,
            65,
            anchor="nw",
            text="VEYLLISTO",
            fill=PRIMARY,
            font=TITLE_FONT,
        )

        canvas.create_text(
            62,
            115,
            anchor="nw",
            text=subtitle,
            fill=SECONDARY,
            font=SUBTITLE_FONT,
        )

        canvas.create_line(
            60,
            155,
            840,
            155,
            fill=SECONDARY,
        )

    def show_welcome():
        nonlocal selected, current_screen

        current_screen = "welcome"
        selected = 0

        clear_screen()
        draw_header("FIRST-LAUNCH EXPERIENCE")

        canvas.create_text(
            60,
            200,
            anchor="nw",
            text=(
                "Welcome to Veyllisto.\n\n"
                "Choose how you would like to configure your system."
            ),
            fill=PRIMARY,
            font=SUBTITLE_FONT,
        )

        redraw_welcome()

    def redraw_welcome():
        canvas.delete("menu")

        canvas.create_text(
            90,
            315,
            anchor="nw",
            text=("> " if selected == 0 else "  ") + OPTIONS[0][0],
            fill=ACCENT if selected == 0 else PRIMARY,
            font=MENU_FONT,
            tags="menu",
        )

        canvas.create_text(
            115,
            350,
            anchor="nw",
            text=OPTIONS[0][1],
            fill=SECONDARY,
            font=INFO_FONT,
            tags="menu",
        )

        canvas.create_text(
            90,
            415,
            anchor="nw",
            text=("> " if selected == 1 else "  ") + OPTIONS[1][0],
            fill=ACCENT if selected == 1 else PRIMARY,
            font=MENU_FONT,
            tags="menu",
        )

        canvas.create_text(
            115,
            450,
            anchor="nw",
            text=OPTIONS[1][1],
            fill=SECONDARY,
            font=INFO_FONT,
            tags="menu",
        )

        canvas.create_text(
            60,
            550,
            anchor="nw",
            text="↑↓ MOVE     ENTER SELECT",
            fill=SECONDARY,
            font=INFO_FONT,
            tags="menu",
        )

    def show_power_user_confirm():
        nonlocal selected, current_screen

        current_screen = "power_confirm"

        # Default to NO so skipping setup requires an intentional choice.
        selected = 1

        clear_screen()
        draw_header("POWER USER SETUP")

        canvas.create_text(
            60,
            200,
            anchor="nw",
            text=(
                "Skip guided configuration?\n\n"
                "Veyllisto will continue using the current system defaults.\n"
                "Setup can be opened again later from Settings."
            ),
            fill=PRIMARY,
            font=SUBTITLE_FONT,
        )

        redraw_power_confirm()

    def redraw_power_confirm():
        canvas.delete("menu")

        canvas.create_text(
            90,
            350,
            anchor="nw",
            text=("> " if selected == 0 else "  ") + "YES — CONTINUE",
            fill=ACCENT if selected == 0 else PRIMARY,
            font=MENU_FONT,
            tags="menu",
        )

        canvas.create_text(
            90,
            415,
            anchor="nw",
            text=("> " if selected == 1 else "  ") + "NO — GO BACK",
            fill=ACCENT if selected == 1 else PRIMARY,
            font=MENU_FONT,
            tags="menu",
        )

        canvas.create_text(
            60,
            550,
            anchor="nw",
            text="↑↓ MOVE     ENTER SELECT     ESC BACK",
            fill=SECONDARY,
            font=INFO_FONT,
            tags="menu",
        )

    def handle_key(event):
        nonlocal selected, result

        if current_screen == "welcome":
            if event.keysym == "Up":
                selected = (selected - 1) % len(OPTIONS)
                redraw_welcome()

            elif event.keysym == "Down":
                selected = (selected + 1) % len(OPTIONS)
                redraw_welcome()

            elif event.keysym == "Return":
                if selected == 0:
                    result = "beginner"
                    root.destroy()
                else:
                    show_power_user_confirm()

        elif current_screen == "power_confirm":
            if event.keysym == "Up":
                selected = (selected - 1) % 2
                redraw_power_confirm()

            elif event.keysym == "Down":
                selected = (selected + 1) % 2
                redraw_power_confirm()

            elif event.keysym == "Escape":
                show_welcome()

            elif event.keysym == "Return":
                if selected == 0:
                    result = "power_user_confirmed"
                    root.destroy()
                else:
                    show_welcome()

    root.bind("<Key>", handle_key)

    show_welcome()

    root.mainloop()

    return result


if __name__ == "__main__":
    run()