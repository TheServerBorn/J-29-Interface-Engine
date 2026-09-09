from tkinter import Tk, Label, Canvas

from engine.core import J29Engine
from pathlib import Path

import time
engine = J29Engine()
identity = engine.get_identity()
settings = engine.get_settings()
theme = engine.get_theme()

games = engine.get_games()
library = engine.get_library()

root = Tk()

root.title(identity["os_name"])
root.configure(bg=theme["background"])
root.geometry("800x500")
root.attributes("-fullscreen", settings["fullscreen"])

def maintenance_mode(event=None):
    engine.play_sound("access_granted")
    engine.set_aux_display("MAINTENANCE", "J-29", "MAINTENANCE")
    root.attributes("-fullscreen", False)
    root.config(cursor="")

def shutdown_terminal(event=None):
    engine.set_aux_display("SHUTDOWN", "J-29", "SHUTDOWN")
    # Give the short async shutdown tone a moment to start before Tk exits.
    # This is intentionally tiny and does not affect normal navigation or
    # external game-launch timing.
    engine.play_sound("shutdown")
    root.after(220, root.destroy)

def terminal_mode(event=None):
    engine.set_aux_display("READY", "J-29", "READY")
    root.attributes("-fullscreen", True)
    root.config(cursor="none")

root.bind(f"<{settings['windowed_key']}>", maintenance_mode)
root.bind(f"<{settings['fullscreen_key']}>", terminal_mode)
root.protocol("WM_DELETE_WINDOW", shutdown_terminal)

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

def get_prompt_y():
    menu_box = scanline_canvas.bbox(canvas_menu)

    if menu_box:
        return menu_box[3] + 30

    return 290

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

def update_command_display():
    prompt_y = get_prompt_y()

    scanline_canvas.coords(
        canvas_command,
        60,
        prompt_y
    )

    scanline_canvas.itemconfig(
        canvas_command,
        text="> " + command_buffer
    )

    command_box = scanline_canvas.bbox(canvas_command)

    if command_box:
        scanline_canvas.coords(
            canvas_cursor,
            command_box[2] + 4,
            prompt_y
        )

def start_command_mode():
    global command_mode, command_buffer

    command_mode = True
    command_buffer = ""

    set_footer("ENTER RUN   ESC CANCEL")
    update_command_display()

def stop_command_mode():
    global command_mode, command_buffer

    command_mode = False
    command_buffer = ""

    scanline_canvas.itemconfig(
        canvas_command,
        text=""
    )

    scanline_canvas.coords(
        canvas_cursor,
        60,
        get_prompt_y()
    )

    update_footer()

def change_directory(target):

    target = target.strip().upper()

    if not target:
        show_temporary_status(
            "USAGE: CD <DIRECTORY>",
            duration=2000
        )
        return

    # Enter the root of the virtual game filesystem.
    if target in ("/", "GAMES", "GAMES/"):

        if current_screen != "games":
            remember_current_screen()

        show_game_library()
        return

    # Move up from a library folder to GAMES/.
    if target == "..":

        if current_screen != "games":
            remember_current_screen()

        show_game_library()
        return

    # Open a valid library folder.
    if target in library:

        if current_screen != "games":
            remember_current_screen()

        show_game_library(target)
        return

    show_temporary_status(
        "DIRECTORY NOT FOUND",
        duration=2000
    )

def show_directory_listing():

    if current_screen == "games":

        draw_game_library()

        if current_library_folder is None:
            show_temporary_status(
                "DIRECTORY: GAMES/",
                duration=2000
            )
        else:
            show_temporary_status(
                f"DIRECTORY: GAMES/{current_library_folder}/",
                duration=2000
            )

        return

    remember_current_screen()
    show_game_library()

    show_temporary_status(
        "DIRECTORY: GAMES/",
        duration=2000
    )

def execute_command():
    global command_mode, command_buffer

    command = command_buffer.strip().upper()

    command_mode = False
    command_buffer = ""

    scanline_canvas.itemconfig(
        canvas_command,
        text=""
    )

    scanline_canvas.itemconfig(
        canvas_cursor,
        state="normal"
    )

    scanline_canvas.coords(
        canvas_cursor,
        60,
        get_prompt_y()
    )

    if command == "HELP":
        remember_current_screen()
        show_command_help()

    elif command == "GAMES":
        remember_current_screen()
        show_game_library()

    elif command in ("FAVORITES", "FAV"):
        remember_current_screen()
        show_favorites()

    elif command in ("RECENT", "RECENTS"):
        remember_current_screen()
        show_recent()

    elif command == "DIR":
        show_directory_listing()

    elif command == "LS":
        show_directory_listing()

    elif command == "CD":
        change_directory("")

    elif command.startswith("CD "):
        change_directory(
            command[3:]
        )

    elif command == "SYSINFO":
        remember_current_screen()
        show_system_info()

    elif command in ("AUX", "AUXDISPLAY", "DISPLAY"):
        remember_current_screen()
        show_aux_display_diagnostics()

    elif command == "BACK":

        if (
            current_screen == "games"
            and current_library_folder is not None
        ):
            show_game_library()

        else:
            go_back()

    elif command == "CLEAR":
        clear_current_screen()

    elif command == "REBOOT":
        reboot_terminal()

    elif command == "SHUTDOWN":
        shutdown_terminal()

    else:
        engine.play_sound("error")
        show_temporary_status("UNKNOWN COMMAND")

def reboot_terminal():
    global command_mode, command_buffer, screen_history

    command_mode = False
    command_buffer = ""
    screen_history = []

    scanline_canvas.itemconfig(
        canvas_command,
        text=""
    )

    start_boot_sequence(aux_state="REBOOTING")

def handle_command_input(event):
    global command_buffer

    if event.keysym == "Escape":
        stop_command_mode()
        return

    if event.keysym == "Return":
        execute_command()
        return

    if event.keysym == "BackSpace":
        command_buffer = command_buffer[:-1]
        update_command_display()
        return

    if event.char and event.char.isprintable():
        command_buffer += event.char.upper()
        update_command_display()

def update_footer():

    if current_screen == "main":
        set_footer("↑↓ MOVE   ENTER SELECT")

    elif current_screen == "games":

        if current_library_folder is None:
            set_footer(
                "↑↓ MOVE   ENTER OPEN   ESC BACK"
            )
        else:
            set_footer(
                "↑↓ MOVE   ENTER RUN   ESC BACK"
            )

    elif current_screen == "favorites":
        set_footer("↑↓ MOVE   ENTER INFO   F REMOVE   ESC BACK")

    elif current_screen == "recent":
        set_footer("↑↓ MOVE   ENTER INFO   ESC BACK")

    elif current_screen == "game_details":
        set_footer("ENTER RUN   F FAVORITE   ESC BACK")

    elif current_screen == "system":
        set_footer("ESC BACK")

    elif current_screen == "aux_display":
        set_footer("↑↓ MOVE   ENTER SELECT   R REFRESH   ESC BACK")

    elif current_screen == "media_prompt":
        set_footer("Y/ENTER OPEN   N/ESC IGNORE")

    elif current_screen == "media_collection":
        set_footer("↑↓ MOVE   ENTER RUN   ESC CLOSE")

    elif current_screen == "media_tools":
        set_footer("↑↓ MOVE   ENTER SELECT   ESC BACK")

    elif current_screen == "media_creator_groups":
        set_footer("↑↓ MOVE   ENTER OPEN   ESC BACK")

    elif current_screen == "media_creator_games":
        set_footer("↑↓ MOVE   ENTER SELECT   ESC LIBRARIES")

    elif current_screen == "media_creator_collection_games":
        if len(creator_collection_selection) < 2:
            set_footer("↑↓ MOVE   SPACE TOGGLE   SELECT 2+ TO CONTINUE   ESC LIBRARIES")
        else:
            set_footer("↑↓ MOVE   SPACE TOGGLE   ENTER NEXT   ESC LIBRARIES")

    elif current_screen == "media_creator_collection_title":
        set_footer("TYPE NAME   ENTER NEXT   ESC BACK")

    elif current_screen == "media_creator_collection_order":
        set_footer("↑↓ SELECT   ←→ REORDER   ENTER PREVIEW   ESC BACK")

    elif current_screen in ("media_creator_preview", "media_creator_collection_preview"):
        set_footer("ENTER TARGET   ESC BACK")

    elif current_screen == "media_creator_targets":
        set_footer("↑↓ MOVE   ENTER SELECT   R REFRESH   ESC BACK")

    elif current_screen == "media_creator_confirm":
        if creator_selected_target and creator_selected_target.get("existing_descriptor"):
            set_footer("R REPLACE   ESC CANCEL")
        else:
            set_footer("W WRITE   ESC CANCEL")

    elif current_screen == "media_creator_replace_confirm":
        set_footer("W REPLACE   ESC CANCEL")

    elif current_screen == "media_creator_result":
        set_footer("ENTER DONE   ESC BACK")

    else:
        set_footer("")

def clear_current_screen():

    scanline_canvas.itemconfig(
        canvas_command,
        text=""
    )

    update_footer()

    if current_screen == "main":
        draw_main_menu()

    elif current_screen == "games":
        draw_game_library()

    elif current_screen == "favorites":
        draw_favorites()

    elif current_screen == "recent":
        draw_recent()

    elif current_screen == "game_details":
        if selected_game_record:
            show_game_details(selected_game_record)

    elif current_screen == "system":
        show_system_info()

    elif current_screen == "aux_display":
        draw_aux_display_diagnostics()

    elif current_screen == "help":
        show_command_help()

    elif current_screen == "media_prompt":
        draw_media_prompt()

    elif current_screen == "media_collection":
        draw_media_collection()

    elif current_screen == "media_tools":
        draw_media_tools()

    elif current_screen == "media_creator_groups":
        draw_media_creator_groups()

    elif current_screen == "media_creator_games":
        draw_media_creator_games()

    elif current_screen == "media_creator_collection_games":
        draw_media_collection_game_picker()

    elif current_screen == "media_creator_collection_title":
        draw_media_collection_title()

    elif current_screen == "media_creator_collection_order":
        draw_media_collection_order()

    elif current_screen == "media_creator_preview":
        draw_media_creator_preview()

    elif current_screen == "media_creator_collection_preview":
        draw_media_collection_preview()

    elif current_screen == "media_creator_targets":
        draw_media_creator_targets()

    elif current_screen == "media_creator_confirm":
        draw_media_creator_confirm()

    elif current_screen == "media_creator_replace_confirm":
        draw_media_creator_replace_confirm()

    elif current_screen == "media_creator_result":
        draw_media_creator_result()


def get_aux_display_options():
    return [
        ("TEST DISPLAY", "test"),
        ("RELOAD ADAPTER", "reload"),
        ("BACK", "back"),
    ]


def show_aux_display_diagnostics(reset_selection=True):
    global current_screen, selected_aux_option

    current_screen = "aux_display"
    if reset_selection:
        selected_aux_option = 0

    scanline_canvas.itemconfig(canvas_cursor, state="normal")
    set_title(
        "========================================\n"
        "        AUXILIARY DISPLAY\n"
        "========================================"
    )
    draw_aux_display_diagnostics()
    scanline_canvas.coords(canvas_cursor, 60, get_prompt_y())


def draw_aux_display_diagnostics():
    try:
        status = engine.get_aux_display_status()
    except Exception as exc:
        status = {
            "enabled": False,
            "adapter": "UNKNOWN",
            "available": False,
            "error": str(exc),
        }

    current_settings = engine.get_settings()
    enabled = bool(status.get("enabled"))
    available = bool(status.get("available"))

    if not enabled:
        status_label = "DISABLED"
    elif available:
        status_label = "AVAILABLE"
    else:
        status_label = "UNAVAILABLE"

    adapter = str(status.get("adapter") or "NONE").upper()
    width = current_settings.get("aux_display_width", 16)
    port = str(current_settings.get("aux_display_serial_port") or "—")
    error = str(status.get("error") or "NONE")

    lines = [
        f"STATUS .......... {status_label}",
        f"ADAPTER ......... {adapter}",
        f"WIDTH ........... {width}",
        f"PORT ............ {port}",
        f"LAST ERROR ...... {error}",
        "",
    ]

    for index, (label, _action) in enumerate(get_aux_display_options()):
        marker = "> " if index == selected_aux_option else "  "
        lines.append(marker + label)

    set_menu("\n".join(lines))
    update_footer()


def test_aux_display_from_ui():
    try:
        success = engine.test_aux_display()
    except Exception:
        success = False

    if success:
        engine.play_sound("access_granted")
        show_temporary_status("DISPLAY TEST SENT", duration=1800)
    else:
        engine.play_sound("error")
        status = engine.get_aux_display_status()
        show_temporary_status(
            status.get("error") or "DISPLAY UNAVAILABLE",
            duration=2500,
        )

    draw_aux_display_diagnostics()


def reload_aux_display_from_ui():
    try:
        engine.reload_aux_display()
        status = engine.get_aux_display_status()

        if status.get("available"):
            engine.play_sound("access_granted")
            show_temporary_status("AUX DISPLAY RELOADED", duration=1800)
        elif status.get("enabled"):
            engine.play_sound("error")
            show_temporary_status(
                status.get("error") or "DISPLAY UNAVAILABLE",
                duration=2500,
            )
        else:
            show_temporary_status("AUX DISPLAY DISABLED", duration=1800)

    except Exception as exc:
        engine.play_sound("error")
        show_temporary_status(str(exc), duration=2500)

    draw_aux_display_diagnostics()


def get_media_tool_options():
    return [
        ("CREATE MEDIA", "create_media"),
        ("CREATE COLLECTION", "create_collection"),
        ("BACK", "back"),
    ]


def show_media_tools():
    global current_screen, selected_media_tool

    current_screen = "media_tools"
    selected_media_tool = 0
    scanline_canvas.itemconfig(canvas_cursor, state="normal")
    set_title(
        "========================================\n"
        "             MEDIA TOOLS\n"
        "========================================"
    )
    draw_media_tools()
    scanline_canvas.coords(canvas_cursor, 60, get_prompt_y())


def draw_media_tools():
    options = get_media_tool_options()
    menu_text = ""

    for index, (label, _action) in enumerate(options):
        marker = "> " if index == selected_media_tool else "  "
        menu_text += marker + label + "\n"

    set_menu(menu_text)
    update_footer()


def _creator_game_title(game):
    return str(
        game.get("title")
        or game.get("name")
        or "PROGRAM"
    ).strip()


def _creator_game_group(game):
    # Steam-discovered titles may report PLATFORM=PC. Keep them separate from
    # native/local PC software so users can tell the launch source at a glance.
    launch_type = str(game.get("launch_type") or "").strip().upper()
    game_id = str(game.get("id") or "").strip().upper()
    folder = str(game.get("folder") or "").strip().upper()

    if launch_type == "STEAM" or game_id.startswith("STEAM_") or folder == "STEAM":
        return "STEAM"

    return str(
        game.get("platform")
        or game.get("folder")
        or "OTHER"
    ).strip().upper() or "OTHER"


def _refresh_creator_library():
    global creator_all_games, creator_library_groups

    creator_all_games = sorted(
        engine.get_media_creator_games(),
        key=lambda game: _creator_game_title(game).casefold(),
    )

    creator_library_groups = sorted({
        _creator_game_group(game)
        for game in creator_all_games
    }, key=str.casefold)


def _creator_entries_for_group(group_name):
    if group_name == "ALL PROGRAMS":
        return list(creator_all_games)

    return [
        game for game in creator_all_games
        if _creator_game_group(game) == group_name
    ]


def show_media_creator_groups(mode="SINGLE", reset_selection=True, refresh=False):
    global current_screen, creator_mode, selected_creator_group
    global creator_browse_group, creator_selected_game, creator_preview
    global creator_collection_selection, creator_collection_title

    creator_mode = mode
    creator_selected_game = None
    creator_preview = None
    creator_browse_group = None

    if refresh or not creator_all_games:
        _refresh_creator_library()

    if mode == "COLLECTION" and reset_selection:
        creator_collection_selection = []
        creator_collection_title = ""

    if reset_selection:
        selected_creator_group = 0

    current_screen = "media_creator_groups"
    scanline_canvas.itemconfig(canvas_cursor, state="normal")
    set_title(
        "========================================\n"
        + (
            "       CREATE MEDIA — COLLECTION\n"
            if mode == "COLLECTION"
            else "            CREATE MEDIA\n"
        )
        + "========================================"
    )
    draw_media_creator_groups()
    scanline_canvas.coords(canvas_cursor, 60, get_prompt_y())


def draw_media_creator_groups():
    entries = list(creator_library_groups) + ["ALL PROGRAMS"]

    if not creator_all_games:
        set_menu("SELECT LIBRARY\n\nNO ELIGIBLE LIBRARY PROGRAMS")
        update_footer()
        return

    capacity = _list_capacity(header_lines=2)
    start, end = _visible_list_window(entries, selected_creator_group, capacity)
    menu_text = (
        "SELECT LIBRARY "
        f"{_range_status(start, end, len(entries))}\n\n"
    )

    for index in range(start, end):
        group_name = entries[index]
        marker = "> " if index == selected_creator_group else "  "
        count = len(_creator_entries_for_group(group_name))
        menu_text += f"{marker}{group_name} ({count})\n"

    set_menu(menu_text)
    update_footer()


def _open_creator_group(group_name):
    global creator_games, creator_browse_group
    global selected_creator_game, selected_creator_collection_game
    global current_screen

    creator_browse_group = group_name
    creator_games = _creator_entries_for_group(group_name)

    if creator_mode == "COLLECTION":
        selected_creator_collection_game = 0
        current_screen = "media_creator_collection_games"
        draw_media_collection_game_picker()
    else:
        selected_creator_game = 0
        current_screen = "media_creator_games"
        draw_media_creator_games()

    scanline_canvas.coords(canvas_cursor, 60, get_prompt_y())


def show_media_creator_games(reset_selection=True):
    # Backward-compatible entry point used by existing return paths.
    show_media_creator_groups(
        mode="SINGLE",
        reset_selection=reset_selection,
        refresh=reset_selection,
    )


def draw_media_creator_games():
    entries = creator_games

    if not entries:
        set_menu("SELECT PROGRAM\n\nNO PROGRAMS IN THIS LIBRARY")
        update_footer()
        return

    capacity = _list_capacity(header_lines=3)
    start, end = _visible_list_window(entries, selected_creator_game, capacity)
    menu_text = (
        f"{creator_browse_group}/\n"
        "SELECT PROGRAM "
        f"{_range_status(start, end, len(entries))}\n\n"
    )

    for index in range(start, end):
        game = entries[index]
        marker = "> " if index == selected_creator_game else "  "
        menu_text += f"{marker}{_creator_game_title(game)}\n"

    set_menu(menu_text)
    update_footer()


def _creator_game_id(game):
    return str((game or {}).get("id") or "").strip()


def _collection_has_game(game):
    game_id = _creator_game_id(game).casefold()
    return any(
        _creator_game_id(item).casefold() == game_id
        for item in creator_collection_selection
    )


def show_media_collection_game_picker(reset_selection=True):
    # Entry from MEDIA TOOLS begins at the shared library browser. Returning
    # from later collection screens can reopen the current library directly.
    if reset_selection or not creator_browse_group:
        show_media_creator_groups(
            mode="COLLECTION",
            reset_selection=reset_selection,
            refresh=reset_selection,
        )
        return

    global current_screen, creator_games, selected_creator_collection_game
    creator_games = _creator_entries_for_group(creator_browse_group)
    selected_creator_collection_game = max(
        0,
        min(selected_creator_collection_game, max(0, len(creator_games) - 1)),
    )
    current_screen = "media_creator_collection_games"
    draw_media_collection_game_picker()
    scanline_canvas.coords(canvas_cursor, 60, get_prompt_y())


def draw_media_collection_game_picker():
    entries = creator_games
    selected_count = len(creator_collection_selection)

    if not entries:
        set_menu(
            f"{creator_browse_group}/\n"
            "SELECT PROGRAMS\n\n"
            "NO PROGRAMS IN THIS LIBRARY"
        )
        update_footer()
        return

    capacity = _list_capacity(header_lines=4)
    start, end = _visible_list_window(
        entries,
        selected_creator_collection_game,
        capacity,
    )
    menu_text = (
        f"{creator_browse_group}/\n"
        f"SELECT PROGRAMS — {selected_count} SELECTED "
        f"{_range_status(start, end, len(entries))}\n\n"
    )

    for index in range(start, end):
        game = entries[index]
        marker = "> " if index == selected_creator_collection_game else "  "
        checked = "[X]" if _collection_has_game(game) else "[ ]"
        menu_text += f"{marker}{checked} {_creator_game_title(game)}\n"

    set_menu(menu_text)
    update_footer()


def toggle_media_collection_game(game):
    global creator_collection_selection

    game_id = _creator_game_id(game).casefold()
    for index, item in enumerate(creator_collection_selection):
        if _creator_game_id(item).casefold() == game_id:
            creator_collection_selection.pop(index)
            return

    creator_collection_selection.append(game)


def show_media_collection_title(reset=False):
    global current_screen, creator_collection_title

    if reset:
        creator_collection_title = ""

    current_screen = "media_creator_collection_title"
    scanline_canvas.itemconfig(canvas_cursor, state="hidden")
    set_title(
        "========================================\n"
        "       CREATE MEDIA — COLLECTION\n"
        "========================================"
    )
    draw_media_collection_title()


def draw_media_collection_title():
    shown_title = creator_collection_title or "_"
    set_menu(
        f"PROGRAMS ........ {len(creator_collection_selection)}\n\n"
        "COLLECTION TITLE\n\n"
        f"> {shown_title}\n\n"
        "LEAVE BLANK FOR: J-29 COLLECTION"
    )
    update_footer()


def show_media_collection_order(reset_selection=True):
    global current_screen, selected_creator_collection_order

    if len(creator_collection_selection) < 2:
        engine.play_sound("error")
        show_media_collection_game_picker(reset_selection=False)
        show_temporary_status("SELECT AT LEAST TWO PROGRAMS", duration=1800)
        return

    if reset_selection:
        selected_creator_collection_order = 0
    else:
        selected_creator_collection_order = max(
            0,
            min(selected_creator_collection_order, len(creator_collection_selection) - 1),
        )

    current_screen = "media_creator_collection_order"
    scanline_canvas.itemconfig(canvas_cursor, state="normal")
    set_title(
        "========================================\n"
        "       CREATE MEDIA — COLLECTION\n"
        "========================================"
    )
    draw_media_collection_order()
    scanline_canvas.coords(canvas_cursor, 60, get_prompt_y())


def draw_media_collection_order():
    entries = creator_collection_selection
    capacity = _list_capacity(header_lines=3)
    start, end = _visible_list_window(
        entries,
        selected_creator_collection_order,
        capacity,
    )
    menu_text = (
        f"ORDER PROGRAMS {_range_status(start, end, len(entries))}\n"
        f"TITLE: {creator_collection_title or 'J-29 COLLECTION'}\n\n"
    )

    for index in range(start, end):
        game = entries[index]
        marker = "> " if index == selected_creator_collection_order else "  "
        title = game.get("title") or game.get("name") or "PROGRAM"
        platform_name = game.get("platform") or game.get("folder") or "UNKNOWN"
        menu_text += f"{marker}{index + 1}. {title} [{platform_name}]\n"

    set_menu(menu_text)
    update_footer()


def reorder_media_collection(direction):
    global selected_creator_collection_order

    index = selected_creator_collection_order
    new_index = index + direction
    if new_index < 0 or new_index >= len(creator_collection_selection):
        return

    creator_collection_selection[index], creator_collection_selection[new_index] = (
        creator_collection_selection[new_index],
        creator_collection_selection[index],
    )
    selected_creator_collection_order = new_index
    engine.play_sound("menu_move")
    draw_media_collection_order()


def show_media_collection_preview():
    global current_screen, creator_preview, creator_mode

    creator_mode = "COLLECTION"
    creator_preview = engine.preview_media_collection(
        creator_collection_selection,
        creator_collection_title,
    )
    current_screen = "media_creator_collection_preview"
    scanline_canvas.itemconfig(canvas_cursor, state="hidden")
    set_title(
        "========================================\n"
        "      CREATE COLLECTION — PREVIEW\n"
        "========================================"
    )
    draw_media_collection_preview()


def draw_media_collection_preview():
    if not creator_preview:
        set_menu("NO COLLECTION PREVIEW AVAILABLE")
        update_footer()
        return

    items = creator_preview.get("items", [])
    preview_lines = []
    for index, item in enumerate(items[:6], start=1):
        preview_lines.append(
            f"{index}. {item.get('title', 'PROGRAM')} [{item.get('platform', 'UNKNOWN')}]"
        )
    if len(items) > 6:
        preview_lines.append(f"... {len(items) - 6} MORE")

    set_menu(
        f"MEDIA TYPE ...... {creator_preview['media_type']}\n"
        f"TITLE ........... {creator_preview['title']}\n"
        f"ITEMS ........... {creator_preview['item_count']}\n"
        f"DESCRIPTOR ...... {creator_preview['status']}\n\n"
        + "\n".join(preview_lines)
        + "\n\nNO MEDIA HAS BEEN WRITTEN\n"
        "PRESS ENTER TO SELECT TARGET MEDIA"
    )
    update_footer()


def show_current_creator_preview():
    if creator_mode == "COLLECTION":
        show_media_collection_preview()
    elif creator_selected_game:
        show_media_creator_preview(creator_selected_game)
    else:
        show_media_tools()


def show_media_creator_preview(game):
    global current_screen, creator_selected_game, creator_preview, creator_mode

    creator_mode = "SINGLE"
    creator_selected_game = game
    creator_preview = engine.preview_media_launch_key(game)
    current_screen = "media_creator_preview"
    scanline_canvas.itemconfig(canvas_cursor, state="hidden")
    set_title(
        "========================================\n"
        "        CREATE MEDIA — PREVIEW\n"
        "========================================"
    )
    draw_media_creator_preview()


def draw_media_creator_preview():
    if not creator_preview:
        set_menu("NO MEDIA PREVIEW AVAILABLE")
        update_footer()
        return

    set_menu(
        f"MEDIA TYPE ...... {creator_preview['media_type']}\n"
        f"TITLE ........... {creator_preview['title']}\n"
        f"PLATFORM ........ {creator_preview['platform']}\n"
        f"TARGET .......... {creator_preview['target']}\n"
        f"DESCRIPTOR ...... {creator_preview['status']}\n\n"
        "NO MEDIA HAS BEEN WRITTEN\n"
        "PRESS ENTER TO SELECT TARGET MEDIA"
    )
    update_footer()


def _creator_target_label(target):
    path = target.get("path", "MEDIA")
    label = target.get("label", "")
    text = path
    if label:
        text += f" [{label}]"
    if target.get("existing_descriptor"):
        text += " [J29 DATA EXISTS]"
    return text


def show_media_creator_targets(reset_selection=True):
    global current_screen, creator_targets, selected_creator_target
    global creator_selected_target, creator_write_result

    creator_targets = engine.get_media_creator_targets()
    if reset_selection:
        selected_creator_target = 0
    elif creator_targets:
        selected_creator_target = max(
            0,
            min(selected_creator_target, len(creator_targets) - 1),
        )

    creator_selected_target = None
    creator_write_result = None
    current_screen = "media_creator_targets"
    scanline_canvas.itemconfig(canvas_cursor, state="normal")
    set_title(
        "========================================\n"
        "       CREATE MEDIA — TARGET\n"
        "========================================"
    )
    draw_media_creator_targets()
    scanline_canvas.coords(canvas_cursor, 60, get_prompt_y())


def draw_media_creator_targets():
    entries = creator_targets
    if not entries:
        set_menu(
            "SELECT TARGET MEDIA\n\n"
            "NO SAFE WRITABLE REMOVABLE MEDIA FOUND\n\n"
            "INSERT USB / SD / FLOPPY MEDIA\n"
            "THEN PRESS R TO REFRESH"
        )
        update_footer()
        return

    capacity = _list_capacity(header_lines=2)
    start, end = _visible_list_window(
        entries,
        selected_creator_target,
        capacity,
    )
    menu_text = (
        "SELECT TARGET MEDIA "
        f"{_range_status(start, end, len(entries))}\n\n"
    )

    for index in range(start, end):
        target = entries[index]
        marker = "> " if index == selected_creator_target else "  "
        menu_text += marker + _creator_target_label(target) + "\n"

    set_menu(menu_text)
    update_footer()


def show_media_creator_confirm(target):
    global current_screen, creator_selected_target, creator_existing_summary
    creator_selected_target = target
    creator_existing_summary = None
    if target.get("existing_descriptor"):
        try:
            creator_existing_summary = engine.get_existing_media_summary(target["path"])
        except Exception as exc:
            creator_existing_summary = {
                "exists": True,
                "valid": False,
                "mode": "UNKNOWN",
                "title": "UNREADABLE J-29 METADATA",
                "reason": str(exc),
            }
    current_screen = "media_creator_confirm"
    scanline_canvas.itemconfig(canvas_cursor, state="hidden")
    set_title(
        "========================================\n"
        "        CREATE MEDIA — WRITE\n"
        "========================================"
    )
    draw_media_creator_confirm()


def draw_media_creator_confirm():
    if not creator_selected_target or not creator_preview:
        set_menu("MEDIA CREATOR STATE NOT AVAILABLE")
        update_footer()
        return

    target_text = _creator_target_label(creator_selected_target)
    item_line = ""
    if creator_mode == "COLLECTION":
        item_line = f"ITEMS ........... {creator_preview.get('item_count', 0)}\n"

    if creator_selected_target.get("existing_descriptor"):
        existing = creator_existing_summary or {}
        existing_type = existing.get("mode", "UNKNOWN").replace("_", " ")
        existing_title = existing.get("title") or "UNKNOWN"
        existing_extra = ""
        if existing.get("item_count"):
            existing_extra = f"CURRENT ITEMS ... {existing.get('item_count')}\n"
        if not existing.get("valid", False):
            existing_extra += f"CURRENT STATUS .. {existing.get('reason', 'INVALID METADATA')}\n"
        set_menu(
            f"NEW TYPE ........ {creator_preview['media_type']}\n"
            f"NEW TITLE ....... {creator_preview['title']}\n"
            + item_line
            + f"TARGET .......... {target_text}\n"
            "FILE ............ j29-media.ini\n\n"
            "EXISTING J-29 METADATA DETECTED\n"
            f"CURRENT TYPE .... {existing_type}\n"
            f"CURRENT TITLE ... {existing_title}\n"
            + existing_extra
            + "\nPRESS R TO ENTER REPLACE MODE"
        )
    else:
        set_menu(
            f"TYPE ............ {creator_preview['media_type']}\n"
            f"TITLE ........... {creator_preview['title']}\n"
            + item_line
            + f"TARGET .......... {target_text}\n"
            "FILE ............ j29-media.ini\n\n"
            "WARNING: THIS WILL WRITE TO REMOVABLE MEDIA\n"
            "PRESS W TO WRITE"
        )
    update_footer()



def show_media_creator_replace_confirm():
    global current_screen

    if not creator_selected_target or not creator_selected_target.get("existing_descriptor"):
        engine.play_sound("error")
        return

    current_screen = "media_creator_replace_confirm"
    scanline_canvas.itemconfig(canvas_cursor, state="hidden")
    set_title(
        "========================================\n"
        "       REPLACE J-29 METADATA\n"
        "========================================"
    )
    draw_media_creator_replace_confirm()


def draw_media_creator_replace_confirm():
    existing = creator_existing_summary or {}
    current_type = existing.get("mode", "UNKNOWN").replace("_", " ")
    current_title = existing.get("title") or "UNKNOWN"
    new_title = (creator_preview or {}).get("title", "UNKNOWN")
    new_type = (creator_preview or {}).get("media_type", "UNKNOWN")

    set_menu(
        f"CURRENT TYPE .... {current_type}\n"
        f"CURRENT TITLE ... {current_title}\n\n"
        f"NEW TYPE ........ {new_type}\n"
        f"NEW TITLE ....... {new_title}\n\n"
        "ONLY j29-media.ini WILL BE REPLACED\n"
        "OTHER FILES ON THIS MEDIA WILL NOT BE MODIFIED\n\n"
        "PRESS W TO REPLACE J-29 METADATA"
    )
    update_footer()

def perform_media_creator_write(replace_existing=False):
    global current_screen, creator_write_result

    if not creator_selected_target:
        engine.play_sound("error")
        return

    if creator_mode == "SINGLE" and not creator_selected_game:
        engine.play_sound("error")
        return
    if creator_mode == "COLLECTION" and len(creator_collection_selection) < 2:
        engine.play_sound("error")
        return

    target_has_descriptor = bool(creator_selected_target.get("existing_descriptor"))
    if target_has_descriptor and not replace_existing:
        engine.play_sound("error")
        return
    if replace_existing and not target_has_descriptor:
        engine.play_sound("error")
        return

    try:
        if creator_mode == "COLLECTION":
            if replace_existing:
                creator_write_result = engine.replace_media_collection(
                    creator_collection_selection,
                    creator_collection_title,
                    creator_selected_target["path"],
                )
            else:
                creator_write_result = engine.write_media_collection(
                    creator_collection_selection,
                    creator_collection_title,
                    creator_selected_target["path"],
                )
        else:
            if replace_existing:
                creator_write_result = engine.replace_media_launch_key(
                    creator_selected_game,
                    creator_selected_target["path"],
                )
            else:
                creator_write_result = engine.write_media_launch_key(
                    creator_selected_game,
                    creator_selected_target["path"],
                )
        engine.play_sound("access_granted")
    except Exception as exc:
        creator_write_result = {
            "success": False,
            "replaced": replace_existing,
            "error": str(exc),
            "target_path": creator_selected_target.get("path", "MEDIA"),
        }
        engine.play_sound("error")

    current_screen = "media_creator_result"
    scanline_canvas.itemconfig(canvas_cursor, state="hidden")
    set_title(
        "========================================\n"
        "       CREATE MEDIA — RESULT\n"
        "========================================"
    )
    draw_media_creator_result()


def draw_media_creator_result():
    result = creator_write_result or {}
    if result.get("success"):
        item_line = ""
        if result.get("item_count"):
            item_line = f"ITEMS ........... {result.get('item_count')}\n"
        action_text = "REPLACE COMPLETE" if result.get("replaced") else "WRITE COMPLETE"
        set_menu(
            f"{action_text}\n\n"
            f"TITLE ........... {result.get('title', 'PROGRAM')}\n"
            + item_line
            + f"TARGET .......... {result.get('target_path', 'MEDIA')}\n"
            "FILE ............ j29-media.ini\n"
            "VERIFICATION .... PASS\n\n"
            "REMOVE AND REINSERT MEDIA TO ACTIVATE"
        )
    else:
        action_text = "REPLACE FAILED" if result.get("replaced") else "WRITE FAILED"
        set_menu(
            f"{action_text}\n\n"
            f"TARGET .......... {result.get('target_path', 'MEDIA')}\n"
            f"ERROR ........... {result.get('error', 'UNKNOWN ERROR')}\n\n"
            "NO VERIFIED MEDIA WAS CREATED"
        )
    update_footer()


def _same_volume(left, right):
    return str(left or "").rstrip("\\/").casefold() == str(right or "").rstrip("\\/").casefold()


def _media_key(volume):
    return str(volume or "").rstrip("\\/").casefold()


def _remember_available_media(media):
    volume = media.get("volume")
    if volume:
        available_media[_media_key(volume)] = media


def _forget_available_media(volume):
    available_media.pop(_media_key(volume), None)


def _current_available_media():
    if not available_media:
        return None
    # dicts preserve insertion order; the newest inserted medium is last.
    return next(reversed(available_media.values()))


def _is_recognized_media(media):
    """Avoid treating unrelated fixed/data volumes as J-29 physical media."""
    if not media:
        return False
    if media.get("metadata") is not None:
        return True
    if media.get("game"):
        return True
    if media.get("collection"):
        return True
    return False


def scan_initial_physical_media():
    """Register recognized media that was already mounted before J-29 boot."""
    global selected_option

    try:
        present = engine.get_present_media()
    except Exception:
        present = []

    changed = False
    for media in present:
        if not _is_recognized_media(media):
            continue

        key = _media_key(media.get("volume"))
        if key and key not in available_media:
            _remember_available_media(media)
            changed = True

    # If boot is disabled, the main menu may already be visible. Redraw it so
    # PHYSICAL MEDIA appears immediately. During the normal boot sequence, the
    # eventual main-menu draw will pick up available_media automatically.
    if changed and current_screen == "main":
        options = get_main_menu_options()
        if options:
            selected_option = min(selected_option, len(options) - 1)
        draw_main_menu()


def _remove_queued_media(volume):
    global media_queue
    media_queue = [
        item for item in media_queue
        if not _same_volume(item.get("volume"), volume)
    ]


def handle_removed_media(media):
    """Safely handle removal whether media is queued, prompted, or idle."""
    global pending_media

    volume = media.get("volume")
    name = media.get("volume_name", "MEDIA")

    _remove_queued_media(volume)
    _forget_available_media(volume)

    if pending_media and _same_volume(pending_media.get("volume"), volume):
        pending_media = None
        go_back()
        show_temporary_status(
            f"MEDIA REMOVED: {name}",
            duration=3000
        )
        return

    if current_screen == "main":
        # Remove the dynamic PHYSICAL MEDIA entry immediately when the last
        # mounted medium disappears.
        options = get_main_menu_options()
        if options:
            global selected_option
            selected_option = min(selected_option, len(options) - 1)
        draw_main_menu()

    if current_screen != "media_prompt":
        show_temporary_status(
            f"MEDIA REMOVED: {name}",
            duration=2500
        )


def draw_media_prompt():
    if not pending_media:
        return

    game = pending_media.get("game")
    metadata = pending_media.get("metadata") or {}
    volume_name = pending_media.get("volume_name", "REMOVABLE MEDIA")

    if metadata.get("valid") and metadata.get("type") == "COLLECTION":
        aux_title = (
            pending_media.get("collection_title")
            or metadata.get("title")
            or "COLLECTION"
        )
    elif game:
        aux_title = game.get("name") or game.get("title") or "PROGRAM"
    else:
        aux_title = volume_name

    aux_state = getattr(engine.get_aux_display_state(), "state", "")
    if not aux_game_session_active and aux_state != "LAUNCH_FAILED":
        engine.set_aux_display(
            "MEDIA_DETECTED",
            "MEDIA DETECTED",
            str(aux_title)[:32],
        )

    if metadata.get("valid") and metadata.get("type") == "COLLECTION":
        title = (
            pending_media.get("collection_title")
            or metadata.get("title")
            or "SOFTWARE COLLECTION"
        )
        count = len(pending_media.get("collection") or [])
        set_menu(
            "MEDIA DETECTED\n\n"
            f"{title}\n"
            f"{count} PROGRAM{'S' if count != 1 else ''}\n\n"
            "OPEN COLLECTION?\n"
            "[Y/N]"
        )
    elif game:
        platform_name = game.get("platform") or "UNKNOWN FORMAT"
        set_menu(
            "MEDIA DETECTED\n\n"
            f"{game.get('name', 'UNKNOWN PROGRAM')}\n"
            f"{platform_name}\n\n"
            "LOAD GAME?\n"
            "[Y/N]"
        )
    else:
        count = pending_media.get("candidate_count", 0)

        if metadata and not metadata.get("valid", True):
            detail = metadata.get("reason", "INVALID J-29 MEDIA METADATA")
            resolved_rom = metadata.get("resolved_rom")
            if resolved_rom:
                detail += f"\n\nEXPECTED:\n{resolved_rom}"
        elif count > 1:
            detail = f"{count} PROGRAM FILES DETECTED"
        else:
            detail = "NO RECOGNIZED PROGRAM"

        set_menu(
            "MEDIA DETECTED\n\n"
            f"{volume_name}\n\n"
            f"{detail}\n\n"
            "PRESS ESC"
        )

    update_footer()


def show_media_collection(reset_selection=True):
    global current_screen, selected_media_item

    if not pending_media:
        return

    items = pending_media.get("collection") or []
    if not items:
        return

    if reset_selection:
        selected_media_item = 0
    else:
        selected_media_item = max(0, min(selected_media_item, len(items) - 1))

    current_screen = "media_collection"
    scanline_canvas.itemconfig(canvas_cursor, state="normal")
    set_title(
        "========================================\n"
        "          PHYSICAL MEDIA\n"
        "========================================"
    )
    draw_media_collection()
    scanline_canvas.coords(canvas_cursor, 60, get_prompt_y())


def draw_media_collection():
    if not pending_media:
        return

    items = pending_media.get("collection") or []
    title = pending_media.get("collection_title") or "SOFTWARE COLLECTION"

    if not items:
        set_menu(f"{title}\n\nNO PROGRAMS AVAILABLE")
        update_footer()
        return

    capacity = _list_capacity(header_lines=2)
    start, end = _visible_list_window(items, selected_media_item, capacity)
    menu_text = f"{title} {_range_status(start, end, len(items))}\n\n"

    for i in range(start, end):
        game = items[i]
        marker = "> " if i == selected_media_item else "  "
        platform_name = game.get("platform") or "MEDIA"
        name = game.get("title") or game.get("name") or game.get("target_game_id") or "PROGRAM"
        menu_text += f"{marker}{name} [{platform_name}]\n"

    set_menu(menu_text)
    update_footer()


def launch_selected_media_item():
    if not pending_media:
        return

    items = pending_media.get("collection") or []
    if not items:
        return

    index = max(0, min(selected_media_item, len(items) - 1))
    game = items[index]

    rom_path = game.get("rom_path") or game.get("path")
    if rom_path and not Path(rom_path).exists():
        show_media_collection(reset_selection=False)
        show_temporary_status("MEDIA PROGRAM NOT AVAILABLE")
        return

    def collection_launch_failed():
        show_media_collection(reset_selection=False)
        show_temporary_status(
            engine.get_last_launch_error()
            or "MEDIA PROGRAM NOT AVAILABLE"
        )

    launch_game_with_transition(
        game,
        on_success=lambda: show_media_collection(reset_selection=False),
        on_failure=collection_launch_failed,
    )

def show_media_prompt(media):
    global current_screen, pending_media

    # Do not recursively replace an active media prompt.
    if current_screen == "media_prompt":
        return

    remember_current_screen()
    pending_media = media
    current_screen = "media_prompt"
    set_title(
        "========================================\n"
        "          PHYSICAL MEDIA\n"
        "========================================"
    )
    draw_media_prompt()


def dismiss_media_prompt():
    global pending_media

    pending_media = None
    go_back()

    # If more than one volume arrived during the same polling interval, present
    # them one at a time instead of silently dropping later insertions.
    if media_queue:
        next_media = media_queue.pop(0)
        root.after(100, lambda: show_media_prompt(next_media))



def _launch_display_name(game):
    if not game:
        return "PROGRAM"

    return (
        game.get("title")
        or game.get("name")
        or game.get("id")
        or "PROGRAM"
    )


def _aux_ready_if_session_active():
    global aux_game_session_active, aux_game_process

    if not aux_game_session_active:
        return

    aux_game_session_active = False
    aux_game_process = None
    engine.set_aux_display("READY", "J-29", "READY")


def _poll_aux_game_process():
    """Return the auxiliary display to READY when a tracked process exits."""
    global aux_game_session_active, aux_game_process

    if not aux_game_session_active or aux_game_process is None:
        return

    try:
        running = aux_game_process.poll() is None
    except Exception:
        running = False

    if running:
        root.after(500, _poll_aux_game_process)
    else:
        _aux_ready_if_session_active()


def _aux_focus_return(event=None):
    """Steam fallback: READY when the user returns focus to J-29."""
    if not aux_game_session_active:
        return

    if time.monotonic() - aux_game_session_started < 3.0:
        return

    if engine.get_last_launch_type() == "STEAM":
        _aux_ready_if_session_active()


def _begin_aux_game_session():
    global aux_game_session_active, aux_game_session_started, aux_game_process

    aux_game_session_active = True
    aux_game_session_started = time.monotonic()
    aux_game_process = engine.get_last_launch_process()

    if aux_game_process is not None:
        root.after(500, _poll_aux_game_process)


def _promote_aux_game_running(game):
    """
    Promote LAUNCHING -> RUNNING without delaying the external game itself.

    If a tracked executable/emulator exits before the short visibility window
    ends, _poll_aux_game_process() will already have returned the display to
    READY and this function intentionally does nothing.
    """
    if not aux_game_session_active:
        return

    state = engine.get_aux_display_state()
    if getattr(state, "state", "") != "GAME_LAUNCHING":
        return

    title = str(
        game.get("title")
        or game.get("name")
        or game.get("id")
        or "PROGRAM"
    ).strip()

    engine.set_aux_display("GAME_RUNNING", "RUNNING", title[:32])


def _schedule_aux_launch_failure_reset():
    def reset_if_still_failed():
        state = engine.get_aux_display_state()
        if getattr(state, "state", "") != "LAUNCH_FAILED":
            return

        if current_screen == "media_prompt" and pending_media:
            game = pending_media.get("game") or {}
            metadata = pending_media.get("metadata") or {}
            title = (
                pending_media.get("collection_title")
                or metadata.get("title")
                or game.get("name")
                or game.get("title")
                or pending_media.get("volume_name")
                or "MEDIA"
            )
            engine.set_aux_display("MEDIA_DETECTED", "MEDIA DETECTED", str(title)[:32])
        else:
            engine.set_aux_display("READY", "J-29", "READY")

    root.after(1800, reset_if_still_failed)


def draw_launch_transition(game):
    """Show an immediate acknowledgement while an external program starts."""
    global current_screen

    current_screen = "launching"

    name = str(_launch_display_name(game)).upper()
    launch_type = str(game.get("launch_type", "PROGRAM")).upper()

    set_title(
        "========================================\n"
        "          CALLISTO COMPUTER SYSTEMS\n"
        "========================================"
    )
    set_menu(
        "LAUNCHING PROGRAM...\n\n"
        f"{name}\n"
        f"{launch_type}\n\n"
        "PLEASE WAIT"
    )
    set_footer("")


def launch_game_with_transition(game, on_success=None, on_failure=None):
    """Shared launch path for Steam, ROMs, executables, and physical media."""
    if not game:
        return False

    # Render the acknowledgement before calling the external launcher. This
    # avoids exposing the previous menu during Steam/emulator startup latency.
    draw_launch_transition(game)
    root.update_idletasks()
    engine.play_sound("launch")

    launched = engine.launch_game(game)

    if not launched:
        engine.play_sound("error")
        _schedule_aux_launch_failure_reset()
        if on_failure:
            on_failure()
        else:
            show_temporary_status(
                engine.get_last_launch_error()
                or "PROGRAM NOT AVAILABLE"
            )
        return False

    _begin_aux_game_session()

    # Give GAME_LAUNCHING an intentional, visible window on auxiliary displays.
    # This does NOT delay or block the launched game; only the display state is
    # promoted later.
    root.after(900, lambda g=game: _promote_aux_game_running(g))

    # External launchers normally return control before their window is ready.
    # Keep the launch acknowledgement visible long enough to bridge that gap.
    # The callback restores the correct J-29 screen in the background, so when
    # the external program eventually exits the user returns somewhere sane.
    if on_success:
        root.after(6000, on_success)

    return True

def launch_pending_media():
    if not pending_media:
        return

    metadata = pending_media.get("metadata") or {}
    if metadata.get("valid") and metadata.get("type") == "COLLECTION":
        show_media_collection()
        return

    game = pending_media.get("game")
    if not game:
        dismiss_media_prompt()
        return

    rom_path = game.get("rom_path") or game.get("path")
    if rom_path and not Path(rom_path).exists():
        name = pending_media.get("volume_name", "MEDIA")
        dismiss_media_prompt()
        show_temporary_status(
            f"MEDIA REMOVED: {name}",
            duration=3000
        )
        return

    def media_launch_failed():
        global current_screen

        # launch_game_with_transition() changes the screen to "launching".
        # On failure we must restore the actual media-prompt state, not only
        # redraw its text. Otherwise key_pressed() continues treating the
        # Terminal as "launching" and ignores ESC/N.
        current_screen = "media_prompt"
        draw_media_prompt()
        show_temporary_status(
            engine.get_last_launch_error()
            or "MEDIA PROGRAM NOT AVAILABLE"
        )

    launch_game_with_transition(
        game,
        on_success=dismiss_media_prompt,
        on_failure=media_launch_failed,
    )



def poll_physical_media():
    if media_poll_active:
        try:
            events = engine.poll_media_events()
            for media in events.get("inserted", []):
                volume = media.get("volume")
                _remember_available_media(media)
                engine.play_sound("media_detected")

                already_pending = (
                    pending_media
                    and _same_volume(pending_media.get("volume"), volume)
                )
                already_queued = any(
                    _same_volume(item.get("volume"), volume)
                    for item in media_queue
                )

                if already_pending or already_queued:
                    continue

                if current_screen == "media_prompt" or pending_media:
                    media_queue.append(media)
                else:
                    show_media_prompt(media)

            for media in events.get("removed", []):
                handle_removed_media(media)

        except Exception:
            # Physical-media monitoring must never crash the terminal.
            pass

    root.after(500, poll_physical_media)


def show_temporary_status(text, duration=5000):

    set_status(text)

    root.after(
        duration,
        update_footer
    )

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

canvas_command = scanline_canvas.create_text(
    60,
    290,
    anchor="nw",
    text="",
    fill=green,
    font=(theme["font_family"], CURSOR_FONT_SIZE)
)

current_screen = "main"
selected_option = 0
selected_game = 0
# Cache Favorites/Recent entries while those screens are open so arrow-key
# navigation never re-runs the full game-discovery pipeline.
favorite_view_games = []
recent_view_games = []
current_library_folder = None
selected_game_record = None
selected_media_item = 0
selected_media_tool = 0
selected_aux_option = 0
selected_creator_game = 0
creator_selected_game = None
creator_preview = None
creator_mode = "SINGLE"
creator_games = []
creator_all_games = []
creator_library_groups = []
creator_browse_group = None
selected_creator_group = 0
selected_creator_collection_game = 0
creator_collection_selection = []
creator_collection_title = ""
selected_creator_collection_order = 0
creator_targets = []
selected_creator_target = 0
creator_selected_target = None
creator_existing_summary = None
creator_write_result = None
detail_parent_screen = "games"
detail_parent_folder = None
detail_parent_index = 0
screen_history = []
pending_media = None
media_queue = []
available_media = {}
media_poll_active = True
aux_game_session_active = False
aux_game_session_started = 0.0
aux_game_process = None

def remember_current_screen():
    if current_screen != "boot":
        screen_history.append(current_screen)

def go_back():

    if current_screen == "game_details":
        return_from_game_details()
        return

    # If inside a library directory,
    # BACK moves up to GAMES/ first.
    if (
        current_screen == "games"
        and current_library_folder is not None
    ):
        show_game_library()
        return

    if not screen_history:
        show_main_menu()
        return

    previous = screen_history.pop()

    if previous == "main":
        show_main_menu()

    elif previous == "games":
        show_game_library()

    elif previous == "favorites":
        show_favorites()

    elif previous == "recent":
        show_recent()

    elif previous == "system":
        show_system_info()

    elif previous == "aux_display":
        show_aux_display_diagnostics()

    elif previous == "help":
        show_command_help()

    else:
        show_main_menu()

command_mode = False
command_buffer = ""

def show_main_menu():
    global current_screen, selected_option

    current_screen = "main"
    if not aux_game_session_active:
        engine.set_aux_display("READY", "J-29", "READY")
    selected_option = 0

    scanline_canvas.itemconfig(
        canvas_cursor,
        state="normal"
    )

    set_title(
        "====================================\n"
        f" {identity['os_name'].upper()} v{identity['version']}\n"
        "===================================="
    )

    set_footer("↑↓ MOVE   ENTER SELECT")

    draw_main_menu()

    scanline_canvas.coords(
        canvas_cursor,
        60,
        get_prompt_y()
    )


def get_main_menu_options():
    options = [
        ("GAME LIBRARY", "games"),
        ("FAVORITES", "favorites"),
        ("RECENT GAMES", "recent"),
        ("MEDIA TOOLS", "media_tools"),
    ]

    # Physical media is contextual: it exists only while at least one
    # recognized mounted medium is still present. Dismissing the automatic
    # insertion prompt therefore never makes the medium unreachable.
    if available_media:
        options.append(("PHYSICAL MEDIA", "physical_media"))

    options.extend([
        ("SYSTEM INFO", "system"),
        ("AUX DISPLAY", "aux_display"),
        ("EXIT", "exit"),
    ])
    return options


def reopen_current_physical_media():
    media = _current_available_media()
    if not media:
        show_temporary_status("NO PHYSICAL MEDIA DETECTED", duration=2000)
        draw_main_menu()
        return
    show_media_prompt(media)


def draw_main_menu():

    options = get_main_menu_options()
    menu_text = ""

    for i, (label, _action) in enumerate(options):

        if i == selected_option:
            menu_text += "> " + label + "\n"
        else:
            menu_text += "  " + label + "\n"

    set_menu(menu_text)

def show_game_library(folder=None):

    global current_screen
    global selected_game
    global current_library_folder

    current_screen = "games"
    selected_game = 0
    current_library_folder = folder

    scanline_canvas.itemconfig(
        canvas_cursor,
        state="normal"
    )

    set_title(
        "====================================\n"
        "          GAME LIBRARY\n"
        "===================================="
    )

    update_footer()

    draw_game_library()

    scanline_canvas.coords(
        canvas_cursor,
        60,
        get_prompt_y()
    )


def _list_capacity(header_lines=0):
    """Return a safe number of list rows that will never overlap the footer."""
    height = root.winfo_height()
    if height < 300:
        height = 500

    # The menu begins below the title/header area.
    menu_top = 165

    # Reserve substantially more room than the footer text itself because
    # Tk text baselines/font metrics can extend below the nominal y position.
    footer_reserve = 120
    usable_bottom = height - footer_reserve

    available = max(100, usable_bottom - menu_top)

    # MENU_FONT_SIZE is the configured nominal size; add generous line spacing
    # so the final visible row stays comfortably clear of the help bar.
    line_height = max(MENU_FONT_SIZE + 8, 22)
    total_lines = max(4, int(available / line_height))

    return max(3, total_lines - header_lines)


def _visible_list_window(entries, selected_index, capacity):
    """Center the selected entry whenever possible."""
    count = len(entries)

    if count <= capacity:
        return 0, count

    selected_index = max(0, min(selected_index, count - 1))

    # Keep the cursor near the vertical center of the screen.
    half = capacity // 2
    start = selected_index - half

    # Clamp at the beginning/end while keeping a full window.
    start = max(0, min(start, count - capacity))
    end = start + capacity

    return start, end


def _range_status(start, end, total):
    if total <= 0:
        return ""
    return f"[{start + 1}-{end} OF {total}]"


def draw_game_library():

    if not library:
        set_menu(
            "GAMES/\n\n"
            "NO PROGRAMS AVAILABLE"
        )
        return

    # Root of the virtual filesystem
    if current_library_folder is None:
        folders = list(library.keys())
        capacity = _list_capacity(header_lines=2)
        start, end = _visible_list_window(
            folders,
            selected_game,
            capacity
        )

        menu_text = (
            f"GAMES/ {_range_status(start, end, len(folders))}\n\n"
        )

        for i in range(start, end):
            folder = folders[i]
            marker = "> " if i == selected_game else "  "
            menu_text += f"{marker}[DIR] {folder}\n"

    # Inside a directory
    else:
        folder_games = library.get(
            current_library_folder,
            []
        )

        if not folder_games:
            menu_text = (
                f"GAMES/{current_library_folder}/\n\n"
                "NO PROGRAMS AVAILABLE"
            )
        else:
            capacity = _list_capacity(header_lines=2)
            start, end = _visible_list_window(
                folder_games,
                selected_game,
                capacity
            )

            menu_text = (
                f"GAMES/{current_library_folder}/ "
                f"{_range_status(start, end, len(folder_games))}\n\n"
            )

            for i in range(start, end):
                game = folder_games[i]
                marker = "> " if i == selected_game else "  "
                menu_text += marker + game["name"] + "\n"

    set_menu(menu_text)


def _metadata_value(value):
    if value is None or value == "":
        return "UNKNOWN"
    return str(value)

def show_game_details(game):
    global current_screen
    global selected_game_record

    current_screen = "game_details"
    selected_game_record = game

    scanline_canvas.itemconfig(
        canvas_cursor,
        state="hidden"
    )

    set_title(
        "====================================\n"
        "        PROGRAM INFORMATION\n"
        "===================================="
    )

    year = _metadata_value(game.get("year"))
    genre = _metadata_value(game.get("genre"))
    developer = _metadata_value(game.get("developer"))
    publisher = _metadata_value(game.get("publisher"))
    platform = _metadata_value(game.get("platform"))
    launch_type = _metadata_value(game.get("launch_type"))

    favorite = "YES" if engine.is_favorite(game["id"]) else "NO"

    extra_lines = ""

    if game.get("emulator"):
        extra_lines += f"EMULATOR ........ {game['emulator']}\n"

    if game.get("steam_id"):
        extra_lines += f"STEAM ID ........ {game['steam_id']}\n"

    set_menu(
        f"TITLE ........... {game.get('title') or game.get('name')}\n"
        f"PLATFORM ........ {platform}\n"
        f"YEAR ............ {year}\n"
        f"GENRE ........... {genre}\n"
        f"DEVELOPER ....... {developer}\n"
        f"PUBLISHER ....... {publisher}\n"
        f"LAUNCH TYPE ..... {launch_type}\n"
        f"FAVORITE ........ {favorite}\n"
        f"{extra_lines}"
    )

    update_footer()

def return_from_game_details():
    global selected_game

    index = detail_parent_index

    if detail_parent_screen == "favorites":
        show_favorites()
        entries = favorite_view_games

        if entries:
            selected_game = min(index, len(entries) - 1)
            draw_favorites()
        return

    if detail_parent_screen == "recent":
        selected_id = selected_game_record.get("id") if selected_game_record else None
        show_recent()
        entries = recent_view_games

        if entries:
            matching_index = next(
                (i for i, game in enumerate(entries) if game.get("id") == selected_id),
                None,
            )
            if matching_index is not None:
                selected_game = matching_index
            else:
                selected_game = min(index, len(entries) - 1)
            draw_recent()
        return

    folder = detail_parent_folder
    show_game_library(folder)

    entries = library.get(folder, []) if folder else list(library.keys())

    if entries:
        selected_game = min(index, len(entries) - 1)
        draw_game_library()


def show_favorites():
    global current_screen, selected_game, favorite_view_games

    current_screen = "favorites"
    selected_game = 0
    favorite_view_games = engine.get_favorite_games()

    scanline_canvas.itemconfig(
        canvas_cursor,
        state="normal"
    )

    set_title(
        "====================================\n"
        "            FAVORITES\n"
        "===================================="
    )

    update_footer()
    draw_favorites()

    scanline_canvas.coords(
        canvas_cursor,
        60,
        get_prompt_y()
    )


def draw_favorites():
    favorite_games = favorite_view_games

    if not favorite_games:
        set_menu(
            "NO FAVORITE PROGRAMS\n\n"
            "OPEN A PROGRAM AND PRESS F TO ADD ONE"
        )
        return

    capacity = _list_capacity(header_lines=1)
    start, end = _visible_list_window(
        favorite_games,
        selected_game,
        capacity
    )

    menu_text = f"FAVORITES {_range_status(start, end, len(favorite_games))}\n\n"

    for i in range(start, end):
        game = favorite_games[i]
        marker = "> " if i == selected_game else "  "
        menu_text += marker + game["name"] + "\n"

    set_menu(menu_text)


def toggle_selected_favorite(game):
    is_favorite = engine.toggle_favorite(game["id"])

    if is_favorite:
        show_temporary_status("ADDED TO FAVORITES", duration=2000)
    else:
        show_temporary_status("REMOVED FROM FAVORITES", duration=2000)

    return is_favorite


def show_recent():
    global current_screen, selected_game, recent_view_games

    current_screen = "recent"
    selected_game = 0
    recent_view_games = engine.get_recent_games()

    scanline_canvas.itemconfig(
        canvas_cursor,
        state="normal"
    )

    set_title(
        "====================================\n"
        "          RECENT GAMES\n"
        "===================================="
    )

    update_footer()
    draw_recent()

    scanline_canvas.coords(
        canvas_cursor,
        60,
        get_prompt_y()
    )


def draw_recent():
    recent_games = recent_view_games

    if not recent_games:
        set_menu(
            "NO RECENT GAMES\n\n"
            "LAUNCH A PROGRAM TO ADD IT HERE"
        )
        return

    capacity = _list_capacity(header_lines=1)
    start, end = _visible_list_window(
        recent_games,
        selected_game,
        capacity
    )

    menu_text = f"RECENT {_range_status(start, end, len(recent_games))}\n\n"

    for i in range(start, end):
        game = recent_games[i]
        marker = "> " if i == selected_game else "  "
        menu_text += marker + game["name"] + "\n"

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

def start_boot_sequence(aux_state="BOOTING"):

    global current_screen
    current_screen = "boot"

    aux_state = str(aux_state or "BOOTING").strip().upper()
    if aux_state == "REBOOTING":
        engine.set_aux_display("REBOOTING", "J-29", "REBOOTING")
    else:
        engine.set_aux_display("BOOTING", "J-29", "BOOTING")

    engine.play_sound("boot")
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

def show_command_help():
    global current_screen

    current_screen = "help"

    scanline_canvas.itemconfig(
        canvas_cursor,
        state="hidden"
    )

    set_title(
        "====================================\n"
        "          COMMAND HELP\n"
        "===================================="
    )

    set_menu(
        "AVAILABLE COMMANDS\n\n"
        "HELP\n"
        "GAMES\n"
        "FAVORITES / FAV\n"
        "RECENT / RECENTS\n"
        "DIR\n"
        "LS\n"
        "CD <DIRECTORY>\n"
        "SYSINFO\n"
        "CLEAR\n"
        "BACK\n"
        "REBOOT\n"
        "SHUTDOWN"
    )

    set_footer("ESC BACK")

def key_pressed(event):

    global selected_option, selected_game, selected_media_item, command_mode
    global selected_media_tool, selected_creator_game, selected_creator_target
    global selected_aux_option
    global selected_creator_group
    global selected_creator_collection_game, selected_creator_collection_order
    global creator_collection_title
    global detail_parent_screen, detail_parent_folder, detail_parent_index

    if command_mode:
        handle_command_input(event)
        return

    if (
        event.keysym in ("Up", "Down")
        and current_screen in (
            "main", "games", "favorites", "recent", "media_collection", "aux_display",
            "media_tools", "media_creator_groups", "media_creator_games", "media_creator_targets",
            "media_creator_collection_games", "media_creator_collection_order",
        )
    ):
        engine.play_sound("menu_move")

    if current_screen == "media_prompt":
        key = event.keysym.lower()

        if key in ("y", "return"):
            engine.play_sound("select")
            launch_pending_media()
        elif key in ("n", "escape"):
            dismiss_media_prompt()

        return

    if current_screen == "media_collection":
        items = pending_media.get("collection", []) if pending_media else []
        key = event.keysym.lower()

        if key == "up" and items:
            selected_media_item = (selected_media_item - 1) % len(items)
            draw_media_collection()
        elif key == "down" and items:
            selected_media_item = (selected_media_item + 1) % len(items)
            draw_media_collection()
        elif key == "return" and items:
            launch_selected_media_item()
        elif key in ("escape", "n"):
            dismiss_media_prompt()

        return

    if current_screen == "media_tools":
        options = get_media_tool_options()

        if event.keysym == "Up":
            selected_media_tool = (selected_media_tool - 1) % len(options)
            draw_media_tools()
        elif event.keysym == "Down":
            selected_media_tool = (selected_media_tool + 1) % len(options)
            draw_media_tools()
        elif event.keysym == "Return":
            engine.play_sound("select")
            action = options[selected_media_tool][1]
            if action == "create_media":
                show_media_creator_groups(mode="SINGLE", reset_selection=True, refresh=True)
            elif action == "create_collection":
                show_media_creator_groups(mode="COLLECTION", reset_selection=True, refresh=True)
            else:
                go_back()
        elif event.keysym == "Escape":
            go_back()

        return

    if current_screen == "media_creator_groups":
        entries = list(creator_library_groups) + ["ALL PROGRAMS"]

        if event.keysym == "Up" and entries:
            selected_creator_group = (selected_creator_group - 1) % len(entries)
            draw_media_creator_groups()
        elif event.keysym == "Down" and entries:
            selected_creator_group = (selected_creator_group + 1) % len(entries)
            draw_media_creator_groups()
        elif event.keysym == "Return" and entries:
            engine.play_sound("select")
            _open_creator_group(entries[selected_creator_group])
        elif event.keysym == "Escape":
            show_media_tools()
        return

    if current_screen == "media_creator_collection_games":
        entries = creator_games
        key = event.keysym.lower()

        if key == "up" and entries:
            selected_creator_collection_game = (selected_creator_collection_game - 1) % len(entries)
            draw_media_collection_game_picker()
        elif key == "down" and entries:
            selected_creator_collection_game = (selected_creator_collection_game + 1) % len(entries)
            draw_media_collection_game_picker()
        elif key == "space" and entries:
            engine.play_sound("select")
            toggle_media_collection_game(entries[selected_creator_collection_game])
            draw_media_collection_game_picker()
        elif key == "return":
            if len(creator_collection_selection) >= 2:
                engine.play_sound("select")
                show_media_collection_title(reset=False)
            else:
                engine.play_sound("error")
                show_temporary_status("SELECT AT LEAST TWO PROGRAMS", duration=1800)
        elif key == "escape":
            show_media_creator_groups(mode="COLLECTION", reset_selection=False, refresh=False)
        return

    if current_screen == "media_creator_collection_title":
        key = event.keysym.lower()

        if key == "escape":
            show_media_collection_game_picker(reset_selection=False)
        elif key == "return":
            engine.play_sound("select")
            show_media_collection_order()
        elif key == "backspace":
            creator_collection_title = creator_collection_title[:-1]
            draw_media_collection_title()
        elif event.char and event.char.isprintable() and len(creator_collection_title) < 48:
            creator_collection_title += event.char.upper()
            draw_media_collection_title()
        return

    if current_screen == "media_creator_collection_order":
        entries = creator_collection_selection
        key = event.keysym.lower()

        if key == "up" and entries:
            selected_creator_collection_order = (selected_creator_collection_order - 1) % len(entries)
            draw_media_collection_order()
        elif key == "down" and entries:
            selected_creator_collection_order = (selected_creator_collection_order + 1) % len(entries)
            draw_media_collection_order()
        elif key == "left":
            reorder_media_collection(-1)
        elif key == "right":
            reorder_media_collection(1)
        elif key == "return":
            engine.play_sound("select")
            try:
                show_media_collection_preview()
            except Exception as exc:
                engine.play_sound("error")
                show_temporary_status(str(exc), duration=2500)
        elif key == "escape":
            show_media_collection_title(reset=False)
        return

    if current_screen == "media_creator_collection_preview":
        if event.keysym == "Return":
            engine.play_sound("select")
            show_media_creator_targets()
        elif event.keysym == "Escape":
            show_media_collection_order(reset_selection=False)
        return

    if current_screen == "media_creator_games":
        entries = creator_games

        if event.keysym == "Up" and entries:
            selected_creator_game = (selected_creator_game - 1) % len(entries)
            draw_media_creator_games()
        elif event.keysym == "Down" and entries:
            selected_creator_game = (selected_creator_game + 1) % len(entries)
            draw_media_creator_games()
        elif event.keysym == "Return" and entries:
            engine.play_sound("select")
            show_media_creator_preview(entries[selected_creator_game])
        elif event.keysym == "Escape":
            show_media_creator_groups(mode="SINGLE", reset_selection=False, refresh=False)

        return

    if current_screen == "media_creator_preview":
        if event.keysym == "Return":
            engine.play_sound("select")
            show_media_creator_targets()
        elif event.keysym == "Escape":
            _open_creator_group(creator_browse_group or "ALL PROGRAMS")
        return

    if current_screen == "media_creator_targets":
        entries = creator_targets
        key = event.keysym.lower()

        if key == "up" and entries:
            selected_creator_target = (selected_creator_target - 1) % len(entries)
            draw_media_creator_targets()
        elif key == "down" and entries:
            selected_creator_target = (selected_creator_target + 1) % len(entries)
            draw_media_creator_targets()
        elif key == "return" and entries:
            engine.play_sound("select")
            show_media_creator_confirm(entries[selected_creator_target])
        elif key == "r":
            show_media_creator_targets(reset_selection=False)
        elif key == "escape":
            show_current_creator_preview()
        return

    if current_screen == "media_creator_confirm":
        key = event.keysym.lower()
        if key == "w" and not (creator_selected_target or {}).get("existing_descriptor"):
            perform_media_creator_write()
        elif key == "r" and (creator_selected_target or {}).get("existing_descriptor"):
            engine.play_sound("select")
            show_media_creator_replace_confirm()
        elif key == "escape":
            show_media_creator_targets(reset_selection=False)
        return

    if current_screen == "media_creator_replace_confirm":
        key = event.keysym.lower()
        if key == "w":
            perform_media_creator_write(replace_existing=True)
        elif key == "escape":
            show_media_creator_confirm(creator_selected_target)
        return

    if current_screen == "media_creator_result":
        if event.keysym == "Return":
            show_media_tools()
        elif event.keysym == "Escape":
            show_media_creator_targets(reset_selection=False)
        return

    # F is a screen action in v0.22. Other alphabetic keys still open
    # command mode as before.
    if event.keysym.lower() == "f" and current_screen == "game_details":
        if selected_game_record:
            toggle_selected_favorite(selected_game_record)
            show_game_details(selected_game_record)
        return

    if event.keysym.lower() == "f" and current_screen == "favorites":
        favorite_games = favorite_view_games
        if favorite_games:
            game = favorite_games[selected_game]
            toggle_selected_favorite(game)
            show_favorites()
        return

    if event.char and event.char.isalpha():
        start_command_mode()
        handle_command_input(event)
        return

    if current_screen == "main":
        options = get_main_menu_options()

        if event.keysym == "Up":
            selected_option = (selected_option - 1) % len(options)
            draw_main_menu()

        elif event.keysym == "Down":
            selected_option = (selected_option + 1) % len(options)
            draw_main_menu()

        elif event.keysym == "Return":
            action = options[selected_option][1]
            engine.play_sound("select")

            if action == "games":
                remember_current_screen()
                show_game_library()

            elif action == "favorites":
                remember_current_screen()
                show_favorites()

            elif action == "recent":
                remember_current_screen()
                show_recent()

            elif action == "media_tools":
                remember_current_screen()
                show_media_tools()

            elif action == "physical_media":
                reopen_current_physical_media()

            elif action == "system":
                remember_current_screen()
                show_system_info()

            elif action == "aux_display":
                remember_current_screen()
                show_aux_display_diagnostics()

            elif action == "exit":
                shutdown_terminal()

    elif current_screen == "games":

        if current_library_folder is None:
            entries = list(library.keys())
        else:
            entries = library.get(
                current_library_folder,
                []
            )

        if event.keysym == "Up":

            if not entries:
                return

            selected_game -= 1

            if selected_game < 0:
                selected_game = len(entries) - 1

            draw_game_library()

        elif event.keysym == "Down":

            if not entries:
                return

            selected_game += 1

            if selected_game >= len(entries):
                selected_game = 0

            draw_game_library()

        elif event.keysym == "Return":

            if not entries:
                return

            engine.play_sound("select")

            # Root directory:
            # Enter opens a folder
            if current_library_folder is None:

                folder = entries[selected_game]

                show_game_library(folder)

            # Inside a folder:
            # Enter opens the program metadata screen.
            # The details screen owns the explicit RUN action.
            else:

                game = entries[selected_game]
                detail_parent_screen = "games"
                detail_parent_folder = current_library_folder
                detail_parent_index = selected_game
                show_game_details(game)

        elif event.keysym == "Escape":

            # If inside a folder, return to GAMES/
            if current_library_folder is not None:
                show_game_library()

            # If already at GAMES/, leave library
            else:
                go_back()

    elif current_screen == "launching":
        # External program handoff is in progress. Ignore terminal navigation
        # until the scheduled background restore occurs.
        return

    elif current_screen == "game_details":

        if event.keysym == "Return":
            if not selected_game_record:
                return

            game_to_launch = selected_game_record

            def restore_game_details():
                if game_to_launch:
                    show_game_details(game_to_launch)

            def game_launch_failed():
                if game_to_launch:
                    show_game_details(game_to_launch)
                show_temporary_status(
                    engine.get_last_launch_error()
                    or "PROGRAM NOT AVAILABLE"
                )

            launch_game_with_transition(
                game_to_launch,
                on_success=restore_game_details,
                on_failure=game_launch_failed,
            )

        elif event.keysym == "Escape":
            return_from_game_details()

    elif current_screen == "favorites":
        favorite_games = favorite_view_games

        if event.keysym == "Up":
            if not favorite_games:
                return

            selected_game -= 1
            if selected_game < 0:
                selected_game = len(favorite_games) - 1
            draw_favorites()

        elif event.keysym == "Down":
            if not favorite_games:
                return

            selected_game += 1
            if selected_game >= len(favorite_games):
                selected_game = 0
            draw_favorites()

        elif event.keysym == "Return":
            if not favorite_games:
                return

            engine.play_sound("select")
            game = favorite_games[selected_game]
            detail_parent_screen = "favorites"
            detail_parent_folder = None
            detail_parent_index = selected_game
            show_game_details(game)

        elif event.keysym == "Escape":
            go_back()

    elif current_screen == "recent":
        recent_games = recent_view_games

        if event.keysym == "Up":
            if not recent_games:
                return

            selected_game -= 1
            if selected_game < 0:
                selected_game = len(recent_games) - 1
            draw_recent()

        elif event.keysym == "Down":
            if not recent_games:
                return

            selected_game += 1
            if selected_game >= len(recent_games):
                selected_game = 0
            draw_recent()

        elif event.keysym == "Return":
            if not recent_games:
                return

            engine.play_sound("select")
            game = recent_games[selected_game]
            detail_parent_screen = "recent"
            detail_parent_folder = None
            detail_parent_index = selected_game
            show_game_details(game)

        elif event.keysym == "Escape":
            go_back()

    elif current_screen == "aux_display":
        options = get_aux_display_options()

        if event.keysym == "Up":
            selected_aux_option = (selected_aux_option - 1) % len(options)
            draw_aux_display_diagnostics()

        elif event.keysym == "Down":
            selected_aux_option = (selected_aux_option + 1) % len(options)
            draw_aux_display_diagnostics()

        elif event.keysym.lower() == "r":
            reload_aux_display_from_ui()

        elif event.keysym == "Return":
            engine.play_sound("select")
            action = options[selected_aux_option][1]

            if action == "test":
                test_aux_display_from_ui()
            elif action == "reload":
                reload_aux_display_from_ui()
            else:
                go_back()

        elif event.keysym == "Escape":
            go_back()

    elif current_screen == "system":

        if event.keysym == "Escape":
            go_back()

    elif current_screen == "help":

        if event.keysym == "Escape":
            go_back()

def blink_cursor():
    current_text = scanline_canvas.itemcget(canvas_cursor, "text")

    if current_text == cursor_character:
        scanline_canvas.itemconfig(canvas_cursor, text="")
    else:
        scanline_canvas.itemconfig(canvas_cursor, text=cursor_character)

    root.after(500, blink_cursor)


def run():
    root.bind("<Key>", key_pressed)
    root.bind("<FocusIn>", _aux_focus_return, add="+")
    engine.set_aux_display("BOOTING", "J-29", "BOOTING")

    if settings["boot_sequence"]:
        start_boot_sequence()
    else:
        show_main_menu()

    blink_cursor()

    # Detect recognized media that was already mounted before J-29 started.
    # This populates the dynamic PHYSICAL MEDIA menu entry without requiring
    # the user to remove/reinsert the medium after boot.
    root.after(250, scan_initial_physical_media)

    # Start the physical-media polling chain. poll_physical_media() schedules
    # its own next run every two seconds, but it must be invoked once here
    # when the Terminal UI starts.
    root.after(500, poll_physical_media)

    root.mainloop()