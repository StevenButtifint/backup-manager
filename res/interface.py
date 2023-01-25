import tkinter as tk


def make_frame(frame, bg, rw, rh, rx, ry, anchor):
    new_frame = tk.Frame(frame, bg=bg)
    new_frame.place(relwidth=rw, relheight=rh, relx=rx, rely=ry, anchor=anchor)
    return new_frame


