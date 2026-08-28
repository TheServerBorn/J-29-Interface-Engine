from tkinter import Tk, Label

root = Tk()

root.title("J-29 Terminal OS")
root.configure(bg="black")
root.geometry("800x500")

green = "#39FF14"
current_screen = "main"


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
    global current_screen
    current_screen = "main"

    title.config(
        text="====================================\n"
             "       J-29 TERMINAL OS v0.1\n"
             "===================================="
    )

    menu.config(
        text="1. GAME LIBRARY\n"
             "2. SYSTEM INFO\n"
             "3. EXIT\n\n"
             ">"
    )

    status.config(text="")


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
             "ESC. RETURN TO MAIN MENU\n\n"
             ">"
    )

    status.config(text="")


def key_pressed(event):

    if current_screen == "main":

        if event.char == "1":
            show_game_library()

        elif event.char == "2":
            status.config(text="SYSTEM INFO SELECTED")

        elif event.char == "3":
            root.destroy()

    elif current_screen == "games":

        if event.char == "1":
            status.config(text="TEST GAME SELECTED")

        elif event.keysym == "Escape":
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