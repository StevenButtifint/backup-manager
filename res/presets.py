

class Presets:
    def __init__(self):
        self.saved_presets = self.get_saved_presets()
        self.selected_preset = None
        self.recommended_presets = []
        self.recommended_preset_names = []

