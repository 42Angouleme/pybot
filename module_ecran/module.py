#!/bin/python3
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sys
import os

from pathlib import Path

window = tk.Tk()


def bind_events():
    window.bind("q", close)
    window.bind("<Escape>", close)


def draw_buttons():
    label = tk.Label(window, text="Hello Tkinter 1!")
    tk.Button(window, text="Close the Window", font=(
        "Calibri", 14, "bold"), command=close).pack(pady=20)
    label.pack()
    tk.Button(window, text="Close the Window", font=(
        "Calibri", 14, "bold"), command=close).pack(pady=10)
    label2 = tk.Label(window, text="Hello Tkinter 2!")
    label2.pack()


def init_window():
    window.attributes('-fullscreen', True)
    window.title("Python Robot")
    width = window.winfo_screenwidth()
    height = window.winfo_screenheight()
    window.geometry("%dx%d" % (width, height))


def close(event=''):
    # print(event)
    window.destroy()
    window.quit()
    sys.exit()


# def tab():

#     tabControl = ttk.Notebook(window)

#     tab1 = ttk.Frame(tabControl)
#     tab2 = ttk.Frame(tabControl)

#     tabControl.add(tab1, text='Tab 1')
#     tabControl.add(tab2, text='Tab 2')
#     tabControl.pack(expand=1, fill="both")

#     ttk.Label(tab1,
#               text="Welcome to  GeeksForGeeks").grid(column=0,
#                                                      row=0,
#                                                      padx=30,
#                                                      pady=30)
#     ttk.Label(tab2,
#               text="Lets dive into the world of computers").grid(column=0,
#                                                                  row=0,
#                                                                  padx=30,
#                                                                  pady=30)


def canvas():
    canvas = tk.Canvas(window, width=230, height=230)
    img_path = os.getcwd() + "/module_ecran/emoji_ok.png"
    # img_path = str(Path.cwd()) + "/module_ecran/emoji_ok.png"
    # img = tk.PhotoImage(Image.open(img_path))
    img = tk.PhotoImage(file=img_path)
    # canvas.create_image(10, 10, anchor=tk.NW, image=img)
    canvas.create_image(230, 230, image=img)
    canvas.pack()


def run():
    bind_events()
    init_window()
    # draw_buttons()
    # tab()
    canvas()
    window.mainloop()


if __name__ == "__main__":
    run()
