import tkinter as tk
from tkinter import ttk
import tkinter.font as font



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


def make_entry(frame, width, bg, fg, text, rx, ry, anchor):
    entry = tk.Entry(frame, width=width, bg=bg, fg=fg, textvariable=text)
    entry.config(font="Arial 16")
    entry.place(relx=rx, rely=ry, anchor=anchor)
    return entry


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


def set_style():
    a = ttk.Style()
    a.theme_use("clam")
    a.configure('.',            # every class of object
                relief='flat',  # flat ridge for separator
                borderwidth=0,
                highlightthickness=0)

    a.configure("Treeview",
                background="red",
                foreground=TREE_HEADING_BG,
                fieldbackground=TREE_COLUMNS_BG,
                borderwidth=0,
                highlightthickness=0)

    a.configure('Treeview.Heading',
                background=TREE_HEADING_BG,
                foreground=TREE_HEADING_FG)



def make_tree_view(frame, column_names, column_widths):

    tree_view = ttk.Treeview(frame, columns=column_names, show='headings')
    for index, name in enumerate(column_names):
        tree_view.heading(name, text=name)
        tree_view.column(name, width=column_widths[index])
    tree_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree_view.yview)
    tree_view.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
    return tree_view




def make_label(frame, text, bg, fg, rx, ry, anchor, size):
    label = tk.Label(frame, text=text, bg=bg, fg=fg)
    label.place(relx=rx, rely=ry, anchor=anchor)
    label['font'] = font.Font(family="Arial", size=size)
    return label


def make_notebook(frame, tab_names, notebook_bg, notebook_fg):
    nb_style = ttk.Style()
    nb_style.theme_use("clam")
    nb_style.layout("TNotebook", [])
    nb_style.configure("TNotebook", highlightbackground="#848a98",
                    tabmargins=0)  # borderwidth = 0, highlightthickness = 0)

    nb_style.configure("TNotebook",
                       background=NOTEBOOK_BG,
                       fieldbackground="purple",
                       tabmargins=[0, 0, 10, 0],
                       borderwidth=0,
                       highlightthickness=0)

    nb_style.configure("TNotebook.Tab",
                       background=NOTEBOOK_BG,
                       font=('Arial', '16'))
    notebook = ttk.Notebook(frame)
    tabs = []

    for tab_name in tab_names:
        new_tab = tk.Frame(notebook)
        notebook.add(new_tab, text=tab_name)
        tabs.append(new_tab)

    notebook.pack(expand=1, fill="both")

    return notebook, tabs

