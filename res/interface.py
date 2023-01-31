import tkinter as tk


def make_frame(frame, bg, rw, rh, rx, ry, anchor):
    new_frame = tk.Frame(frame, bg=bg)
    new_frame.place(relwidth=rw, relheight=rh, relx=rx, rely=ry, anchor=anchor)
    return new_frame


def make_button(frame, text, height, width, bg, fg, rx, ry, command, size, anchor):
    new_button = tk.Button(frame, text=text, height=height, width=width, bg=bg, fg=fg)
    new_button.config(activebackground=BUTTON_BG_CLICKED, command=command)
    new_button['font'] = font.Font(family='Helvetica', size=size)
    new_button['borderwidth'] = 1
    new_button.place(relx=rx, rely=ry, anchor=anchor)
    new_button.bind("<Enter>", mouse_enter)
    new_button.bind("<Leave>", mouse_leave)
    return new_button


def make_img_button(frame, text, height, width, bg, fg, rx, ry, anchor, command, size, image_dir):
    image = tk.PhotoImage(file=image_dir)
    new_button = tk.Button(frame, text=text, height=height, width=width, bg=bg, fg=fg, image=image)
    new_button.config(activebackground=BUTTON_BG_CLICKED, command=command)
    new_button.image = image
    new_button['font'] = font.Font(family='Helvetica', size=size)
    new_button['borderwidth'] = 1
    new_button.place(relx=rx, rely=ry, anchor=anchor)
    new_button.bind("<Enter>", mouse_enter)
    new_button.bind("<Leave>", mouse_leave)
    return new_button




def make_label(frame, text, bg, fg, rx, ry, anchor, size):
    label = tk.Label(frame, text=text, bg=bg, fg=fg)
    label.place(relx=rx, rely=ry, anchor=anchor)
    label['font'] = font.Font(family="Arial", size=size)
    return label


