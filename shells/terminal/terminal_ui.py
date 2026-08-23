from tkinter import Tk, Label, Canvas

from engine.core import J29Engine

engine = J29Engine()
identity = engine.get_identity()
settings = engine.get_settings()
theme = engine.get_theme()

games = engine.get_games()

root = Tk()

root.title(identity["os_name"])
root.configure(bg=theme["background"])
root.geometry("800x500")
root.attributes("-fullscreen", settings["fullscreen"])

def maintenance_mode(event=None):
    root.attributes("-fullscreen", False)
    root.config(cursor="")

def terminal_mode(event=None):
    root.attributes("-fullscreen", True)
    root.config(cursor="none")

root.bind(f"<{settings['windowed_key']}>", maintenance_mode)
root.bind(f"<{settings['fullscreen_key']}>", terminal_mode)

root.config(cursor="none")
scanline_canvas = Canvas(
    root,
    bg=theme["background"],
    highlightthickness=0
)

scanline_canvas.place(
    x=0,
    y=0,
    relwidth=1,
    relheight=1
)
def draw_scanlines(event=None):

    width = root.winfo_width()
    height = root.winfo_height()

    # Keep the dynamic footer near the bottom of the window
    scanline_canvas.coords(
        canvas_status,
        60,
        height - 60
    )

    scanline_canvas.delete("scanline")

    if not theme["scanlines"]:
        return

    for y in range(0, height, theme["scanline_spacing"]):
        scanline_canvas.create_line(
            0,
            y,
            width,
            y,
            fill=theme["secondary"],
            tags="scanline"
        )

    scanline_canvas.tag_lower("scanline")


root.bind("<Configure>", draw_scanlines)
root.after(100, draw_scanlines)
green = theme["primary"]
TITLE_FONT_SIZE = theme["title_size"]
MENU_FONT_SIZE = theme["menu_size"]
STATUS_FONT_SIZE = theme["status_size"]
CURSOR_FONT_SIZE = theme["cursor_size"]
canvas_title = scanline_canvas.create_text(
    60,
    50,
    anchor="nw",
    text="",
    fill=green,
    font=(theme["font_family"], TITLE_FONT_SIZE, "bold")
)


def set_title(text):
    scanline_canvas.itemconfig(
        canvas_title,
        text=text
    )
canvas_menu = scanline_canvas.create_text(
    60,
    165,
    anchor="nw",
    text="",
    fill=green,
    font=(theme["font_family"], MENU_FONT_SIZE)
)


def set_menu(text):
    scanline_canvas.itemconfig(
        canvas_menu,
        text=text
    )

canvas_status = scanline_canvas.create_text(
    60,
    330,
    anchor="nw",
    text="",
    fill=green,
    font=(theme["font_family"], STATUS_FONT_SIZE)
)

def set_status(text):
    scanline_canvas.itemconfig(
        canvas_status,
        text=text
    )

def set_footer(text):
    if settings["show_footer"]:
        set_status(text)
    else:
        set_status("")

cursor_styles = {
    "BLOCK": "█",
    "UNDERSCORE": "_",
    "BAR": "|",
}

cursor_character = cursor_styles.get(
    theme["cursor_style"].upper(),
    "█"
)

canvas_cursor = scanline_canvas.create_text(
    60,
    360,
    anchor="nw",
    text=cursor_character,
    fill=green,
    font=(theme["font_family"], CURSOR_FONT_SIZE)
)

current_screen = "main"
selected_option = 0
selected_game = 0

def show_main_menu():
    global current_screen, selected_option

    current_screen = "main"
    selected_option = 0
    scanline_canvas.itemconfig(canvas_cursor, state="normal")
    scanline_canvas.coords(canvas_cursor, 60, 290)

    set_title( "====================================\n" f" {identity['os_name'].upper()} v{identity['version']}\n" "====================================" )

    set_footer("↑↓ MOVE   ENTER SELECT")
    draw_main_menu()


def draw_main_menu():

    options = [
        "GAME LIBRARY",
        "SYSTEM INFO",
        "EXIT"
    ]

    menu_text = ""

    for i, option in enumerate(options):

        if i == selected_option:
            menu_text += "> " + option + "\n"
        else:
            menu_text += "  " + option + "\n"

    set_menu(menu_text)


def show_game_library():

    global current_screen, selected_game

    current_screen = "games"
    selected_game = 0

    set_title(
    "====================================\n"
    "          GAME LIBRARY\n"
    "===================================="
)

    set_footer("↑↓ MOVE   ENTER RUN   ESC BACK")
    draw_game_library()

def draw_game_library():

    if not games:
        set_menu("NO PROGRAMS AVAILABLE")
        return

    menu_text = ""

    for i, game in enumerate(games):

        if i == selected_game:
            menu_text += "> " + game["name"] + "\n"
        else:
            menu_text += "  " + game["name"] + "\n"


    set_menu(menu_text)


def show_system_info():

    global current_screen

    current_screen = "system"
    scanline_canvas.itemconfig(canvas_cursor, state="hidden")

    info = engine.get_system_info()

    cpu = info["cpu"]

    if not cpu:
        cpu = "UNKNOWN PROCESSOR"

    os_name = info["os_name"]
    memory_gb = info["memory_gb"]
    system_drive = info["system_drive"]
    total_gb = info["total_gb"]
    free_gb = info["free_gb"]

    set_title(
        "====================================\n"
        "          SYSTEM INFO\n"
        "===================================="
    )

    owner_line = ""
    location_line = ""

    if identity["owner"]:
        owner_line = f"OWNER ........... {identity['owner']}\n"

    if identity["location"]:
        location_line = f"LOCATION ........ {identity['location']}\n"

    set_menu(
        f"MANUFACTURER .... {identity['manufacturer']}\n"
        f"MODEL ........... {identity['model']}\n"
        f"UNIT ID ......... {identity['unit_id']}\n"
        f"SYSTEM .......... {identity['os_name']} v{identity['version']}\n"
        f"{owner_line}"
        f"{location_line}\n"
        f"HOST OS ......... {os_name}\n"
        f"CPU ............. {cpu}\n"
        f"MEMORY .......... {memory_gb} GB\n"
        f"STORAGE ({system_drive}) ... {total_gb} GB\n"
        f"FREE SPACE ...... {free_gb} GB\n"
        f"NETWORK ......... DISABLED\n\n"
    )

    set_footer("ESC BACK")

def start_boot_sequence():

    global current_screen
    current_screen = "boot"
    scanline_canvas.itemconfig(canvas_cursor, state="hidden")
    set_title(
    f"{identity['manufacturer'].upper()}\n"
    f"{identity['model'].upper()}"
)

    set_menu("")
    set_status("")

    info = engine.get_system_info()

    cpu = info["cpu"]
    memory_gb = info["memory_gb"]
    system_drive = info["system_drive"]
    total_gb = info["total_gb"]

    boot_lines = [
        "INITIALIZING SYSTEM...",
        "",
        f"CPU ............ {cpu}",
        f"MEMORY ......... {memory_gb} GB",
        f"STORAGE ........ {total_gb} GB",
        f"SYSTEM DRIVE ... {system_drive}",
        "DISPLAY ........ OK",
        "NETWORK ........ DISABLED",
        "OFFLINE MODE ... ACTIVE",
        "",
        "BOOTING TERMINAL..."
    ]

    def show_line(index=0):

        if index < len(boot_lines):

            current_text = scanline_canvas.itemcget(canvas_menu, "text")

            set_menu(
                current_text + boot_lines[index] + "\n"
            )

            root.after(
                450,
                lambda: show_line(index + 1)
            )

        else:
            root.after(1000, show_main_menu)

    show_line()

def key_pressed(event):

    global selected_option, selected_game

    if current_screen == "main":

        if event.keysym == "Up":
            selected_option -= 1

            if selected_option < 0:
                selected_option = 2

            draw_main_menu()

        elif event.keysym == "Down":
            selected_option += 1

            if selected_option > 2:
                selected_option = 0

            draw_main_menu()

        elif event.keysym == "Return":

            if selected_option == 0:
                show_game_library()

            elif selected_option == 1:
                show_system_info()

            elif selected_option == 2:
                root.destroy()

    elif current_screen == "games":

        if event.keysym == "Up":

            if not games:
                return

            selected_game -= 1

            if selected_game < 0:
                selected_game = len(games) - 1

            draw_game_library()

        elif event.keysym == "Down":

            if not games:
                return

            selected_game += 1

            if selected_game >= len(games):
                selected_game = 0

            draw_game_library()

        elif event.keysym == "Return":

            if not games:
                return

            game_path = games[selected_game]["path"]

            if not engine.launch_game(game_path):
                set_status("PROGRAM NOT AVAILABLE")

        elif event.keysym == "Escape":
            show_main_menu()

    elif current_screen == "system":

        if event.keysym == "Escape":
            show_main_menu()

def blink_cursor():
    current_text = scanline_canvas.itemcget(canvas_cursor, "text")

    if current_text == cursor_character:
        scanline_canvas.itemconfig(canvas_cursor, text="")
    else:
        scanline_canvas.itemconfig(canvas_cursor, text=cursor_character)

    root.after(500, blink_cursor)


def run():
    root.bind("<Key>", key_pressed)

    if settings["boot_sequence"]:
        start_boot_sequence()
    else:
        show_main_menu()

    blink_cursor()

    root.mainloop()