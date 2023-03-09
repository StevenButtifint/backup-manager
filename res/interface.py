import tkinter as tk
from tkinter import ttk
import tkinter.font as font


from res.constants import *


def make_frame(frame, bg, rw, rh, rx, ry, anchor):
    new_frame = tk.Frame(frame, bg=bg)
    new_frame.place(relwidth=rw, relheight=rh, relx=rx, rely=ry, anchor=anchor)
    return new_frame


def make_static_frame(frame, bg, w, h, x, y, anchor):
    new_frame = tk.Frame(frame, bg=bg)
    new_frame.place(width=w, height=h, x=x, y=y, anchor=anchor)
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

    a.layout("TNotebook", [])
    a.configure("TNotebook",
                background=NOTEBOOK_BG,
                highlightbackground="#848a98",
                tabmargins=0)  # borderwidth = 0, highlightthickness = 0)

    a.configure("TNotebook.Tab",
                background=TAB_BG,
                foreground=TAB_FG,
                padding=[20, 5, 20, 2],
                font=('Arial', '16'))

    a.map("TNotebook.Tab",
          padding=[("selected", [20, 5, 20, 2])],
          background=[("selected", TAB_BG_SELECTED)])



def make_tree_view(frame, column_names, column_widths):

    tree_view = ttk.Treeview(frame, columns=column_names, show='headings')
    for index, name in enumerate(column_names):
        tree_view.heading(name, text=name)
        tree_view.column(name, width=column_widths[index], anchor='c')
    tree_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree_view.yview)
    tree_view.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
    return tree_view


def set_tree_view(tree_view, content):
    for i in tree_view.get_children():
        tree_view.delete(i)
    for item in content:
        tree_view.insert('', tk.END, values=item)


def make_listbox(frame, font_size, bg, fg):
    listbox = tk.Listbox(frame, font=("Arial", font_size), bg=bg, fg=fg)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
    listbox.config(yscrollcommand=scrollbar.set)
    listbox.config(highlightthickness=0)
    scrollbar.config(command=listbox.yview)
    return listbox


def set_listbox(listbox, content):
    listbox.delete(0, tk.END)
    listbox.insert(tk.END, *content)


def make_text_box(frame, bg, fg, height, width):
    text_box = tk.Text(frame, bg=bg, fg=fg, height=height, width=width, font=("Arial", 16))
    text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
    return text_box


def make_progress_bar(frame, rx, ry, length, anchor):
    bar = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=length, mode='determinate')
    bar.config()
    bar.place(relx=rx, rely=ry, anchor=anchor)
    return bar


def make_label(frame, text, bg, fg, rx, ry, anchor, size):
    label = tk.Label(frame, text=text, bg=bg, fg=fg)
    label.place(relx=rx, rely=ry, anchor=anchor)
    label['font'] = font.Font(family="Arial", size=size)
    return label


def make_checkbutton(frame, text, size, bg, command, rx, ry, anchor):
    check_value = tk.IntVar()
    checkbutton = tk.Checkbutton(frame, text=text, command=command, variable=check_value, bg=bg)
    checkbutton.place(relx=rx, rely=ry, anchor=anchor)
    checkbutton['font'] = font.Font(family="Arial", size=size)
    return checkbutton, check_value


def make_notebook(frame, tab_names, notebook_bg, notebook_fg):


    notebook = ttk.Notebook(frame)
    tabs = []

    for tab_name in tab_names:
        new_tab = tk.Frame(notebook)
        notebook.add(new_tab, text=tab_name)
        tabs.append(new_tab)

    notebook.pack(expand=1, fill="both")

    return notebook, tabs

def make_option_menu(frame, options, default_idx, x, y, anchor, bg):#NOTUSED_
    string_var = tk.StringVar(frame)
    string_var.set(options[default_idx])
    option_menu = tk.OptionMenu(frame, string_var, *options)
    option_menu.config(bg=bg)
    option_menu["menu"].config(bg=bg)
    option_menu["highlightthickness"]=0
    # option_menu.config(bg=bg, highlightthickness=0, activebackground=BUTTON_BG_HOVER)
    # option_menu["menu"].config(borderwidth=0, bg=bg)
    option_menu["borderwidth"]=1
    option_menu.place(x=x, y=y, anchor=anchor)
    return option_menu


def mouse_enter(e):
    if e.widget['background'] != BUTTON_BG_CLICKED:
        e.widget['background'] = BUTTON_BG_HOVER


def mouse_leave(e):
    if e.widget['background'] != BUTTON_BG_CLICKED:
        e.widget['background'] = BUTTON_BG


def mouse_release(e):
    e.widget['background'] = BUTTON_BG_CLICKED


def mouse_enter_tile(e):#NOTUSED_
    e.widget.config(borderwidth=3)


def mouse_leave_tile(e):#NOTUSED_
    e.widget.config(borderwidth=1)


