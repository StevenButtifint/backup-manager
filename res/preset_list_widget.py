from PyQt5.QtWidgets import *


class PresetList:
    def __init__(self, q_list_widget):
        self.list_widget = q_list_widget

    def clear_list(self):
        self.list_widget.clear()

    def set_list(self, item_list):
        self.clear_list()
        self.list_widget.addItems(item_list)
