from tkinter import Tk, Label, Canvas

import subprocess

import configparser

import platform

import shutil

import os

import ctypes

import winreg

from engine.system_info import (
    get_cpu_name as engine_get_cpu_name,
    get_memory_gb as engine_get_memory_gb
)

config = configparser.ConfigParser()
config.read("games.ini")

games = []

for section in config.sections():
    games.append({
        "name": config[section]["name"],
        "path": config[section]["path"]
    })

root = Tk()

root.title("J-29 Terminal OS")
root.configure(bg="black")
root.geometry("800x500")
root.attributes("-fullscreen", True)

def maintenance_mode(event=None):
    root.attributes("-fullscreen", False)
    root.config(cursor="")

def terminal_mode(event=None):
    root.attributes("-fullscreen", True)
    root.config(cursor="none")

root.bind("<F12>", maintenance_mode)
root.bind("<F11>", terminal_mode)

root.config(cursor="none")
scanline_canvas = Canvas(
    root,
    bg="black",
    highlightthickness=0
)

scanline_canvas.place(
    x=0,
    y=0,
    relwidth=1,
    relheight=1
)
def draw_scanlines(event=None):

    scanline_canvas.delete("scanline")

    width = root.winfo_width()
    height = root.winfo_height()

    for y in range(0, height, 6):
        scanline_canvas.create_line(
            0,
            y,
            width,
            y,
            fill="#031003",
            tags="scanline"
        )

    scanline_canvas.tag_lower("scanline")


root.bind("<Configure>", draw_scanlines)
root.after(100, draw_scanlines)
green = "#39FF14"
TITLE_FONT_SIZE = 24
MENU_FONT_SIZE = 20
STATUS_FONT_SIZE = 18
CURSOR_FONT_SIZE = 20
canvas_title = scanline_canvas.create_text(
    60,
    50,
    anchor="nw",
    text="",
    fill=green,
    font=("Courier New", TITLE_FONT_SIZE, "bold")
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
    font=("Courier New", MENU_FONT_SIZE)
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
    font=("Courier New", STATUS_FONT_SIZE)
)

def set_status(text):
    scanline_canvas.itemconfig(
        canvas_status,
        text=text
    )

canvas_cursor = scanline_canvas.create_text(
    60,
    360,
    anchor="nw",
    text="█",
    fill=green,
    font=("Courier New", CURSOR_FONT_SIZE)
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

    set_title(
    "====================================\n"
    "       J-29 TERMINAL OS v0.13\n"
    "===================================="
)

    set_status("")
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

    set_status("")
    draw_game_library()

def draw_game_library():

    menu_text = ""

    for i, game in enumerate(games):

        if i == selected_game:
            menu_text += "> " + game["name"] + "\n"
        else:
            menu_text += "  " + game["name"] + "\n"

    menu_text += "\nESC. RETURN TO MAIN MENU"

    set_menu(menu_text)

def get_cpu_name():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"
        )

        cpu_name, _ = winreg.QueryValueEx(key, "ProcessorNameString")
        winreg.CloseKey(key)

        return cpu_name.strip()

    except Exception:
        return platform.processor()

def get_memory_gb():
    class MEMORYSTATUSEX(ctypes.Structure):
        _fields_ = [
            ("dwLength", ctypes.c_ulong),
            ("dwMemoryLoad", ctypes.c_ulong),
            ("ullTotalPhys", ctypes.c_ulonglong),
            ("ullAvailPhys", ctypes.c_ulonglong),
            ("ullTotalPageFile", ctypes.c_ulonglong),
            ("ullAvailPageFile", ctypes.c_ulonglong),
            ("ullTotalVirtual", ctypes.c_ulonglong),
            ("ullAvailVirtual", ctypes.c_ulonglong),
            ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
        ]

    memory_status = MEMORYSTATUSEX()
    memory_status.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory_status))

    return round(memory_status.ullTotalPhys / (1024 ** 3))

def show_system_info():

    global current_screen

    current_screen = "system"
    scanline_canvas.itemconfig(canvas_cursor, state="hidden")

    cpu = engine_get_cpu_name()

    if not cpu:
        cpu = "UNKNOWN PROCESSOR"

    os_name = platform.system() + " " + platform.release()

    memory_gb = engine_get_memory_gb()

    system_drive = os.environ.get("SystemDrive", "C:") + "\\"

    total, used, free = shutil.disk_usage(system_drive)

    total_gb = round(total / (1024 ** 3))
    free_gb = round(free / (1024 ** 3))

    set_title(
    "====================================\n"
    "          SYSTEM INFO\n"
    "===================================="
)

    set_menu(
    f"OS .............. {os_name}\n"
    f"CPU ............. {cpu}\n"
    f"MEMORY .......... {memory_gb} GB\n"
    f"STORAGE ({system_drive}) ... {total_gb} GB\n"
    f"FREE SPACE ...... {free_gb} GB\n"
    f"NETWORK ......... DISABLED\n\n"
    "ESC. RETURN TO MAIN MENU"
)

    set_status("")

def start_boot_sequence():

    global current_screen
    current_screen = "boot"
    scanline_canvas.itemconfig(canvas_cursor, state="hidden")
    set_title(
    "CALLISTO COMPUTER SYSTEMS\n"
    "J-29 PERSONAL TERMINAL"
)

    set_menu("")
    set_status("")

    cpu = engine_get_cpu_name()
    memory_gb = engine_get_memory_gb()

    system_drive = os.environ.get("SystemDrive", "C:") + "\\"
    total, used, free = shutil.disk_usage(system_drive)
    total_gb = round(total / (1024 ** 3))

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
            selected_game -= 1

            if selected_game < 0:
                selected_game = len(games) - 1

            draw_game_library()

        elif event.keysym == "Down":
            selected_game += 1

            if selected_game >= len(games):
                selected_game = 0

            draw_game_library()

        elif event.keysym == "Return":

            game_path = games[selected_game]["path"]

            if game_path:
                subprocess.Popen([game_path])
            else:
                set_status("PROGRAM NOT AVAILABLE")

        elif event.keysym == "Escape":
            show_main_menu()

    elif current_screen == "system":

        if event.keysym == "Escape":
            show_main_menu()

def blink_cursor():
    current_text = scanline_canvas.itemcget(canvas_cursor, "text")

    if current_text == "█":
        scanline_canvas.itemconfig(canvas_cursor, text="")
    else:
        scanline_canvas.itemconfig(canvas_cursor, text="█")

    root.after(500, blink_cursor)


root.bind("<Key>", key_pressed)

start_boot_sequence()

blink_cursor()
root.mainloop()