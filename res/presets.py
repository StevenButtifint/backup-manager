
from res.constants import *
from res.operations import resource_path, connected_drive_letters, get_drive_names, get_saved_presets


class Presets:
    def __init__(self):
        self.saved_presets = get_saved_presets()
        self.selected_preset = None
        self.recommended_presets = []
        self.recommended_preset_names = []


    def set_selected_preset(self, preset):
        self.selected_preset = preset

    def clear_selected_preset(self):
        self.selected_preset = None


    @staticmethod
    def get_drive_names():
        drive_names = []
        occupied_letters = connected_drive_letters()
        for letter in occupied_letters:
            drive_names.append(get_drive_name(letter))
        return drive_names

    def update_recommended_presets(self):
        drive_names = get_drive_names()
        self.recommended_presets = []
        self.recommended_preset_names = []
        for preset in self.saved_presets:
            if all(item in drive_names for item in preset["drives"]):
                self.recommended_presets.append(preset)
                self.recommended_preset_names.append(preset["name"])

