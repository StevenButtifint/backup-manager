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
