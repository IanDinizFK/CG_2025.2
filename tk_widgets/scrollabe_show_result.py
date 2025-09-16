from tkinter import *


def scrolable_show_result(root, list, *args, **kwargs):
    frame = Frame(root)
    frame.grid(row=6, column=1, sticky="nsew")

    scroll_bar = Scrollbar(frame)
    scroll_bar.grid(row=0, column=1, sticky="nsew")

    listbox = Listbox(frame, yscrollcommand=scroll_bar.set)
    listbox.grid(row=0, column=0)

    for i in list:
        listbox.insert(END, f"({i[0]}, {i[1]})")

    scroll_bar.config(command=listbox.yview)

    return frame

    