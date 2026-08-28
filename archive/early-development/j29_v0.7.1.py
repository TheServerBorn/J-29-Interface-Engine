from tkinter import Tk, Label

import subprocess

import configparser

import platform

import shutil

import os

import ctypes

import winreg

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

green = "#39FF14"

current_screen = "main"
selected_option = 0
selected_game = 0

title = Label(
    root,
    fg=green,
    bg="black",
    font=("Courier New", 20, "bold"),
    justify="left"
)
title.pack(pady=(40, 20))


menu = Label(
    root,
    fg=green,
    bg="black",
    font=("Courier New", 18),
    justify="left"
)
menu.pack()


status = Label(
    root,
    text="",
    fg=green,
    bg="black",
    font=("Courier New", 16)
)
status.pack(pady=20)


cursor = Label(
    root,
    text="█",
    fg=green,
    bg="black",
    font=("Courier New", 18)
)
cursor.pack()


def show_main_menu():
    global current_screen, selected_option

    current_screen = "main"
    selected_option = 0

    title.config(
        text="====================================\n"
             "       J-29 TERMINAL OS v0.7\n"
             "===================================="
    )

    status.config(text="")
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

    menu.config(text=menu_text)


def show_game_library():

    global current_screen, selected_game

    current_screen = "games"
    selected_game = 0

    title.config(
        text="====================================\n"
             "          GAME LIBRARY\n"
             "===================================="
    )

    status.config(text="")
    draw_game_library()

def draw_game_library():

    menu_text = ""

    for i, game in enumerate(games):

        if i == selected_game:
            menu_text += "> " + game["name"] + "\n"
        else:
            menu_text += "  " + game["name"] + "\n"

    menu_text += "\nESC. RETURN TO MAIN MENU"

    menu.config(text=menu_text)

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

    cpu = get_cpu_name()

    if not cpu:
        cpu = "UNKNOWN PROCESSOR"

    os_name = platform.system() + " " + platform.release()

    memory_gb = get_memory_gb()

    system_drive = os.environ.get("SystemDrive", "C:") + "\\"

    total, used, free = shutil.disk_usage(system_drive)

    total_gb = round(total / (1024 ** 3))
    free_gb = round(free / (1024 ** 3))

    title.config(
        text="====================================\n"
             "          SYSTEM INFO\n"
             "===================================="
    )

    menu.config(
        text=f"OS .............. {os_name}\n"
             f"CPU ............. {cpu}\n"
             f"MEMORY .......... {memory_gb} GB\n"
             f"STORAGE ({system_drive}) ... {total_gb} GB\n"
             f"FREE SPACE ...... {free_gb} GB\n"
             f"NETWORK ......... DISABLED\n\n"
             "ESC. RETURN TO MAIN MENU"
    )

    status.config(text="")

def start_boot_sequence():

    global current_screen
    current_screen = "boot"

    title.config(
        text="CALLISTO COMPUTER SYSTEMS\n"
             "J-29 PERSONAL TERMINAL"
    )

    menu.config(text="")
    status.config(text="")

    boot_lines = [
        "INITIALIZING SYSTEM...",
        "",
        "CPU ............ OK",
        "MEMORY ......... OK",
        "STORAGE ........ OK",
        "DISPLAY ........ OK",
        "NETWORK ........ DISABLED",
        "OFFLINE MODE ... ACTIVE",
        "",
        "BOOTING TERMINAL..."
    ]

    def show_line(index=0):

        if index < len(boot_lines):

            current_text = menu.cget("text")
            menu.config(
                text=current_text + boot_lines[index] + "\n"
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
                status.config(text="PROGRAM NOT AVAILABLE")

        elif event.keysym == "Escape":
            show_main_menu()

    elif current_screen == "system":

        if event.keysym == "Escape":
            show_main_menu()

def blink_cursor():

    if cursor.cget("text") == "█":
        cursor.config(text="")
    else:
        cursor.config(text="█")

    root.after(500, blink_cursor)


root.bind("<Key>", key_pressed)

start_boot_sequence()
blink_cursor()

root.mainloop()