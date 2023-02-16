
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
        make_label(home_frame, APP_VERSION, MAIN_BG, VERSION_FG, 1, 1, "se", 10)

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

    def create_preset_preview(self, name_string, date_created): # change to change content or remake frame each time

    def select_preset_page(self):
        self.presets.clear_selected_preset()
        manage_preset_frame = make_static_frame(self.window, MAIN_BG, APP_EXPANDED_W, APP_EXPANDED_H, 400, 450, "center")
        make_label(manage_preset_frame, "SELECT PRESET", MAIN_BG, TITLE_FG, 0.5, 0.0125, "n", 20)
        presets_frame = make_frame(manage_preset_frame, MAIN_BG, 0.975, 0.235, 0.5, 0.065, "n")
        self.presets_listbox = make_listbox(presets_frame, 18, LISTBOX_BG, LISTBOX_FG)
        self.presets_listbox.bind('<<ListboxSelect>>', self.saved_preset_selected)
        set_listbox(self.presets_listbox, self.presets.get_preset_names())

        preset_details = make_button(manage_preset_frame, "Toggle Preset Details", 1, 17, BUTTON_BG, "black", 0.5, 0.31, lambda: None, 16, "n")
        preset_details.config(command=lambda: self._toggle_preset_details())
        make_button(manage_preset_frame, "Create New Preset", 1, 18, BUTTON_BG, "black", 0.0125, 0.31, lambda: self.create_preset_page(), 16, "nw")
        make_button(manage_preset_frame, "Back", 1, 6, BUTTON_BG, "black", 0.0125, 0.0125, lambda: self._return_to_home(manage_preset_frame), 16, "nw")

        self.preset_preview_frame = make_frame(manage_preset_frame, MAIN_BG_LIGHT, 1, 0.63, 0.5, 1, "s")
        make_label(self.preset_preview_frame, "PRESET DETAILS", MAIN_BG_LIGHT, "black", 0.5, 0.06, "s", 20)
        # self.preset_preview_frame.destroy()
        # self.preset_preview_frame = make_frame(manage_preset_frame, MAIN_BG_LIGHT, 1, 0.63, 0.5, 1, "s")

        self.preset_preview.name = make_label(self.preset_preview_frame, "name_string", MAIN_BG_LIGHT, "black", 0.025, 0.06, "w", 18)
        self.preset_preview.date_created = make_label(self.preset_preview_frame, "Date Created: ", MAIN_BG_LIGHT, "black", 0.06, 0.7, "w", 14)

        make_label(self.preset_preview_frame, "Description:", MAIN_BG_LIGHT, "black", 0.025, 0.1, "w", 18)

        make_label(self.preset_preview_frame, "Location Details", MAIN_BG_LIGHT, "black", 0.5, 0.15, "center", 14)
        column_names = ('Source Locations', 'Backup Locations')
        column_widths = [50, 50]
        preview_tree_frame = make_frame(self.preset_preview_frame, "orange", 0.95, 0.4, 0.5, 0.4, "center")
        self.location_preview_tree = make_tree_view(preview_tree_frame, TREE_NAMES, TREE_WIDTHS)

        self.locations_label = make_label(self.preset_preview_frame, "Sync Locations: ", MAIN_BG_LIGHT, "black", 0.06, 0.65, "w", 14)

        make_button(self.preset_preview_frame, "Delete Preset", 1, 12, BUTTON_BG, "black", 0.5, 0.975, lambda: self.delete_confirm(), 16, "s")


    def _save_new_preset(self, notice, name, description, create_preset_frame):
        notice.config(text="")
        if name == "":
            notice.config(text="Enter a preset name")

        elif name in self.presets.get_preset_names():
            notice.config(text="Preset name must be unique")

        elif len(self.new_preset_locations) == 0:
            notice.config(text="Enter at least one file or folder to sync")

        else:

            preset_drives = []
            for location in self.new_preset_locations:
                new_src = location[5]
                new_dst = location[6]
                if new_src not in preset_drives:
                    preset_drives.append(new_src)
                if new_dst not in preset_drives:
                    preset_drives.append(new_dst)

            print(self.new_preset_locations)

            date_created = datetime.today().strftime('%d-%m-%Y')

            preset_data = '{ "name": '+json.dumps(name)+', "description": '+json.dumps(description)+', "created": ' + json.dumps(date_created) + ' , "locations":' + json.dumps(self.new_preset_locations) + ', "drives":' + json.dumps(preset_drives) + '}'

            preset_data = json.loads(str(preset_data))

            self.presets.save_new_preset(preset_data)

            try:
                set_listbox(self.presets_listbox, self.presets.get_preset_names())
            except:
                pass

            create_preset_frame.destroy()
            self._set_window_compact()





if __name__ == "__main__":
    root = tk.Tk()
    Window(root)
    root.mainloop()
