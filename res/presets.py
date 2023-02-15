

class Presets:
    def __init__(self):
        self.saved_presets = self.get_saved_presets()
        self.selected_preset = None
        self.recommended_presets = []
        self.recommended_preset_names = []


    @staticmethod
    def get_drive_names():
        drive_names = []
        occupied_letters = connected_drive_letters()
        for letter in occupied_letters:
            drive_names.append(get_drive_name(letter))
        return drive_names

