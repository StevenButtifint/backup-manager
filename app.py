
from res.constants import *
from res.interface import *


class Window:
    def __init__(self, parent):
        self.window = parent
        self.window.title(APP_TITLE)
        self.window.resizable(False, False)
        self.window.geometry(APP_DIMS_COMPACT)

    def home_page(self):
        home_frame = make_frame(self.window, MAIN_BG, 1, 1, 0.5, 0.5, "center")

        make_label(home_frame, "WELCOME", MAIN_BG, TITLE_FG, 0.5, 0.03, "n", 20)

        make_img_button(home_frame, "", 200, 200, BUTTON_BG, "black", 0, 0.5, "w", lambda: self.recommend_preset_page(), 12, SEARCH_ICON_DIR)
        make_label(home_frame, "Recommend Preset", MAIN_BG, LABEL_FG, 0.125, 0.86, "center", 14)

        make_img_button(home_frame, "", 200, 200, BUTTON_BG, "black", 0.25, 0.5, "w", lambda: self.manage_preset_page(), 12, TICK_ICON_DIR)
        make_label(home_frame, "Select Preset", MAIN_BG, LABEL_FG, 0.375, 0.86, "center", 14)

        make_img_button(home_frame, "", 200, 200, BUTTON_BG, "black", 0.5, 0.5, "w", lambda: self.create_preset_page(), 12, ADD_ICON_DIR)
        make_label(home_frame, "Create Preset", MAIN_BG, LABEL_FG, 0.625, 0.86, "center", 14)

        make_img_button(home_frame, "", 200, 200, BUTTON_BG, "black", 0.75, 0.5, "w", lambda: quit(), 12, EXIT_ICON_DIR)
        make_label(home_frame, "Quit", MAIN_BG, LABEL_FG, 0.875, 0.86, "center", 14)

    def recommend_preset_page(self):
        occupied_letters = connected_drive_letters()
        drive_names = []
        for letter in occupied_letters:
            drive_names.append(get_drive_name(letter))
        print(drive_names)

        #recommended_presets = []
        recommended_preset_names = []
        for preset in self.presets.saved_presets:
            if all(item in drive_names for item in preset["drives"]):
                #recommended_presets.append(preset)
                recommended_preset_names.append(preset["name"])
                print(preset["name"] + "is available")

        recommend_frame = make_static_frame(self.window, MAIN_BG, APP_EXPANDED_W, APP_EXPANDED_H, 400, 450, "center")
        make_label(recommend_frame, "RECOMMENDED PRESETS", MAIN_BG, TITLE_FG, 0.5, 0.0125, "n", 20)
        make_button(recommend_frame, "Back", 1, 6, BUTTON_BG, "black", 0.0125, 0.0125, lambda: self._return_to_home(recommend_frame), 16, "nw")
        presets_frame = make_frame(recommend_frame, MAIN_BG, 0.975, 0.235, 0.5, 0.065, "n")
        presets_listbox = make_listbox(presets_frame, 18, LISTBOX_BG, LISTBOX_FG)
        set_listbox(presets_listbox, recommended_preset_names)




if __name__ == "__main__":
    root = tk.Tk()
    Window(root)
    root.mainloop()
