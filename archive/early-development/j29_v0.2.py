from tkinter import Tk, Label

root = Tk()

root.title("J-29 Terminal OS")
root.configure(bg="black")
root.geometry("800x500")

green = "#39FF14"

current_screen = "main"
selected_option = 0


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
             "       J-29 TERMINAL OS v0.2\n"
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

    global current_screen

    current_screen = "games"

    title.config(
        text="====================================\n"
             "          GAME LIBRARY\n"
             "===================================="
    )

    menu.config(
        text="1. TEST GAME\n"
             "2. COMING SOON\n\n"
             "ESC. RETURN TO MAIN MENU"
    )

    status.config(text="")

def show_system_info():

    global current_screen

    current_screen = "system"

    title.config(
        text="====================================\n"
             "          SYSTEM INFO\n"
             "===================================="
    )

    menu.config(
        text="J-29 TERMINAL OS v0.2\n"
             "CPU ............ ONLINE\n"
             "MEMORY ......... ONLINE\n"
             "STORAGE ........ ONLINE\n"
             "NETWORK ........ DISABLED\n\n"
             "ESC. RETURN TO MAIN MENU"
    )

    status.config(text="")

def key_pressed(event):

    global selected_option

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

        if event.keysym == "Escape":
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

show_main_menu()
blink_cursor()

root.mainloop()