import tkinter as tk


def make_frame(frame, bg, rw, rh, rx, ry, anchor):
    new_frame = tk.Frame(frame, bg=bg)
    new_frame.place(relwidth=rw, relheight=rh, relx=rx, rely=ry, anchor=anchor)
    return new_frame




def make_label(frame, text, bg, fg, rx, ry, anchor, size):
    label = tk.Label(frame, text=text, bg=bg, fg=fg)
    label.place(relx=rx, rely=ry, anchor=anchor)
    label['font'] = font.Font(family="Arial", size=size)
    return label


