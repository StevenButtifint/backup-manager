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


def make_tree_view(frame, column_names, column_widths):
    a = ttk.Style()

    a.configure('.',            # every class of object
                relief='flat',  # flat ridge for separator
                borderwidth=0,  # zero width for the border
                )

    #a.theme_use("clam")

    a.configure("Treeview",
                #background="red",
                forground=TREE_HEADING_BG,
                fieldbackground=TREE_COLUMNS_BG,
                borderwidth=0,
                highlightthickness=0)

    a.configure('Treeview.Heading',
                background=TREE_HEADING_BG,
                forground="red")

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
    notebook = ttk.Notebook(frame)
    tabs = []

    for tab_name in tab_names:
        new_tab = tk.Frame(notebook)
        notebook.add(new_tab, text=tab_name)
        tabs.append(new_tab)

    notebook.pack(expand=1, fill="both")

    return notebook, tabs

