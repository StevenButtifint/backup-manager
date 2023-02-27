import tkinter as tk


class PresetPreview:
    def __init__(self):
        self.name = tk.Label
        self.description = tk.Text
        self.date_created = tk.Label

    def set_name(self, name):
        self.name.config(text=name)

    def set_date_created(self, date):
        self.date_created.config(text=date)

    def set_description(self, description):
        self.description.config(state=tk.NORMAL)
        self.description.delete(1.0, tk.END)
        self.description.insert(tk.END, description)
        self.description.config(state=tk.DISABLED)

    def clear_attributes(self):
        self.set_name("")
        self.set_date_created("")
        self.set_description("")
