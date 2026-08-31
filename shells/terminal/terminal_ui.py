from tkinter import Tk, Label, Canvas

from engine.core import J29Engine
from pathlib import Path

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
    root.attributes("-fullscreen", False)
    root.config(cursor="")

def shutdown_terminal(event=None):
    # Give the short async shutdown tone a moment to start before Tk exits.
    # This is intentionally tiny and does not affect normal navigation or
    # external game-launch timing.
    engine.play_sound("shutdown")
    root.after(220, root.destroy)

def terminal_mode(event=None):
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

    start_boot_sequence()

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

    elif current_screen == "media_prompt":
        set_footer("Y/ENTER OPEN   N/ESC IGNORE")

    elif current_screen == "media_collection":
        set_footer("↑↓ MOVE   ENTER RUN   ESC CLOSE")

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

    elif current_screen == "help":
        show_command_help()

    elif current_screen == "media_prompt":
        draw_media_prompt()

    elif current_screen == "media_collection":
        draw_media_collection()

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
        if on_failure:
            on_failure()
        else:
            show_temporary_status(
                engine.get_last_launch_error()
                or "PROGRAM NOT AVAILABLE"
            )
        return False

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

    root.after(2000, poll_physical_media)


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
current_library_folder = None
selected_game_record = None
selected_media_item = 0
detail_parent_screen = "games"
detail_parent_folder = None
detail_parent_index = 0
screen_history = []
pending_media = None
media_queue = []
available_media = {}
media_poll_active = True

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

    elif previous == "help":
        show_command_help()

    else:
        show_main_menu()

command_mode = False
command_buffer = ""

def show_main_menu():
    global current_screen, selected_option

    current_screen = "main"
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
    ]

    # Physical media is contextual: it exists only while at least one
    # recognized mounted medium is still present. Dismissing the automatic
    # insertion prompt therefore never makes the medium unreachable.
    if available_media:
        options.append(("PHYSICAL MEDIA", "physical_media"))

    options.extend([
        ("SYSTEM INFO", "system"),
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
        entries = engine.get_favorite_games()

        if entries:
            selected_game = min(index, len(entries) - 1)
            draw_favorites()
        return

    if detail_parent_screen == "recent":
        selected_id = selected_game_record.get("id") if selected_game_record else None
        show_recent()
        entries = engine.get_recent_games()

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
    global current_screen, selected_game

    current_screen = "favorites"
    selected_game = 0

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
    favorite_games = engine.get_favorite_games()

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
    global current_screen, selected_game

    current_screen = "recent"
    selected_game = 0

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
    recent_games = engine.get_recent_games()

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

def start_boot_sequence():

    global current_screen
    current_screen = "boot"
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
    global detail_parent_screen, detail_parent_folder, detail_parent_index

    if command_mode:
        handle_command_input(event)
        return

    if (
        event.keysym in ("Up", "Down")
        and current_screen in ("main", "games", "favorites", "recent", "media_collection")
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

    # F is a screen action in v0.22. Other alphabetic keys still open
    # command mode as before.
    if event.keysym.lower() == "f" and current_screen == "game_details":
        if selected_game_record:
            toggle_selected_favorite(selected_game_record)
            show_game_details(selected_game_record)
        return

    if event.keysym.lower() == "f" and current_screen == "favorites":
        favorite_games = engine.get_favorite_games()
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

            elif action == "physical_media":
                reopen_current_physical_media()

            elif action == "system":
                remember_current_screen()
                show_system_info()

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
        favorite_games = engine.get_favorite_games()

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
        recent_games = engine.get_recent_games()

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
    root.after(1000, poll_physical_media)

    root.mainloop()