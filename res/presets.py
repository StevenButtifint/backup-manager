import json

from res.constants import *
from res.operations import resource_path, connected_drive_letters, get_drive_names, get_saved_presets


class Presets:
    def __init__(self):
        self.saved_presets = get_saved_presets()
        self.selected_preset = None
        self.recommended_presets = []
        self.recommended_preset_names = []

    def get_preset_names(self):
        preset_names = []
        for preset in self.saved_presets:
            preset_names.append(preset["name"])
        return preset_names

    def set_selected_preset(self, preset):
        self.selected_preset = preset

    def clear_selected_preset(self):
        self.selected_preset = None

    def update_recommended_presets(self):
        drive_names = get_drive_names()
        self.recommended_presets = []
        self.recommended_preset_names = []
        for preset in self.saved_presets:
            if all(item in drive_names for item in preset["drives"]):
                self.recommended_presets.append(preset)
                self.recommended_preset_names.append(preset["name"])

    def update_saved_presets(self):
        self.saved_presets = get_saved_presets()

    def delete_preset(self, preset_name):
        for idx, preset in enumerate(self.saved_presets):
            if preset['name'] == preset_name:
                self.saved_presets.pop(idx)

        with open(resource_path(PRESETS_DIR), 'w', encoding='utf-8') as f:
            json.dump(self.saved_presets, f, ensure_ascii=False, indent=4)
        self.update_saved_presets()

