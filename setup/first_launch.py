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
        text="FIRST-LAUNCH EXPERIENCE",
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

    beginner_item = canvas.create_text(
        90,
        315,
        anchor="nw",
        fill=ACCENT,
        font=MENU_FONT,
    )

    canvas.create_text(
        115,
        350,
        anchor="nw",
        text=OPTIONS[0][1],
        fill=SECONDARY,
        font=INFO_FONT,
    )

    power_item = canvas.create_text(
        90,
        415,
        anchor="nw",
        fill=PRIMARY,
        font=MENU_FONT,
    )

    canvas.create_text(
        115,
        450,
        anchor="nw",
        text=OPTIONS[1][1],
        fill=SECONDARY,
        font=INFO_FONT,
    )

    canvas.create_text(
        60,
        550,
        anchor="nw",
        text="↑↓ MOVE     ENTER SELECT",
        fill=SECONDARY,
        font=INFO_FONT,
    )

    def redraw_selection():
        canvas.itemconfig(
            beginner_item,
            text=("> " if selected == 0 else "  ") + OPTIONS[0][0],
            fill=ACCENT if selected == 0 else PRIMARY,
        )

        canvas.itemconfig(
            power_item,
            text=("> " if selected == 1 else "  ") + OPTIONS[1][0],
            fill=ACCENT if selected == 1 else PRIMARY,
        )

    def handle_key(event):
        nonlocal selected

        if event.keysym == "Up":
            selected = (selected - 1) % len(OPTIONS)
            redraw_selection()

        elif event.keysym == "Down":
            selected = (selected + 1) % len(OPTIONS)
            redraw_selection()

        elif event.keysym == "Return":
            nonlocal result

            result = "beginner" if selected == 0 else "power_user"
            root.destroy()

    root.bind("<Key>", handle_key)

    redraw_selection()

    root.mainloop()

    return result

if __name__ == "__main__":
    run()