from res.interface import make_entry, make_button
from res.constants import ENTRY_BG, ENTRY_FG, BUTTON_BG
from res.operations import add_folder, add_file


class LocationPair:
    def __init__(self, frame, src_label, src_func):
        self.src_entry = make_entry(frame, 42, ENTRY_BG, ENTRY_FG, "", 0.01, 0.08, "nw")
        self.dst_entry = make_entry(frame, 42, ENTRY_BG, ENTRY_FG, "", 0.01, 0.28, "nw")

        make_button(frame, src_label, 1, 18, BUTTON_BG, "black", 0.99, 0.05, lambda: src_func(self.src_entry), 16, "ne")
        make_button(frame, "Set Backup Location", 1, 18, BUTTON_BG, "black", 0.99, 0.25, lambda: add_folder(self.dst_entry), 16, "ne")

