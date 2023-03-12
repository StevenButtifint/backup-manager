
from res.constants import *
from res.interface import *
from res.operations import *


class Window:
    def __init__(self, parent):
        self.window = parent
        self.window.title(APP_TITLE)
        self.window.resizable(False, False)
        self.window.geometry(APP_DIMS_COMPACT)
        self.window.iconbitmap(APP_ICON_DIR)
        self.window.config(bg=MAIN_BG)
        self.notice_label = tk.Button()

    def home_page(self):
        set_style()
        home_frame = make_frame(self.window, MAIN_BG, 1, 1, 0.5, 0.5, "center")
        make_label(home_frame, "WELCOME", MAIN_BG, TITLE_FG, 0.5, 0.03, "n", 20)
        make_img_button(home_frame, "", 200, 200, BUTTON_BG, "black", 0, 0.5, "w", lambda: self.recommend_preset_page(), 12, SEARCH_ICON_DIR)
        make_label(home_frame, "Recommend Preset", MAIN_BG, LABEL_FG, 0.125, 0.86, "center", 14)
        make_img_button(home_frame, "", 200, 200, BUTTON_BG, "black", 0.25, 0.5, "w", lambda: self.select_preset_page(), 12, TICK_ICON_DIR)
        make_label(home_frame, "Select Preset", MAIN_BG, LABEL_FG, 0.375, 0.86, "center", 14)
        make_img_button(home_frame, "", 200, 200, BUTTON_BG, "black", 0.5, 0.5, "w", lambda: self.create_preset_page(), 12, ADD_ICON_DIR)
        make_label(home_frame, "Create Preset", MAIN_BG, LABEL_FG, 0.625, 0.86, "center", 14)
        make_img_button(home_frame, "", 200, 200, BUTTON_BG, "black", 0.75, 0.5, "w", lambda: quit(), 12, EXIT_ICON_DIR)
        make_label(home_frame, "Quit", MAIN_BG, LABEL_FG, 0.875, 0.86, "center", 14)
        make_label(home_frame, APP_VERSION, MAIN_BG, VERSION_FG, 1, 1, "se", 10)

    def recommend_preset_page(self):
        self.presets.update_recommended_presets()
        self.presets.clear_selected_preset()
        recommend_frame = make_static_frame(self.window, MAIN_BG, APP_EXPANDED_W, APP_EXPANDED_H, 400, 450, "center")
        make_label(recommend_frame, "RECOMMENDED PRESETS", MAIN_BG, TITLE_FG, 0.5, 0.0125, "n", 20)
        make_button(recommend_frame, "Back", 1, 6, BUTTON_BG, "black", 0.0125, 0.0125, lambda: self._return_to_home(recommend_frame), 16, "nw")
        presets_frame = make_frame(recommend_frame, MAIN_BG, 0.975, 0.235, 0.5, 0.065, "n")
        presets_listbox = make_listbox(presets_frame, 18, LISTBOX_BG, LISTBOX_FG)
        self.notice_label = make_label(recommend_frame, "", MAIN_BG_LIGHT, "red", 0.975, 0.025, "ne", 12)

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
        self.notice_label = make_label(manage_preset_frame, "", MAIN_BG_LIGHT, "red", 0.975, 0.025, "ne", 12)

        preset_preview_frame = make_frame(manage_preset_frame, MAIN_BG_LIGHT, 1, 0.63, 0.5, 1, "s")
        make_label(preset_preview_frame, "PRESET DETAILS", MAIN_BG_LIGHT, LABEL_FG, 0.5, 0.09, "s", 20)

        name_label = make_label(preset_preview_frame, "Name:", MAIN_BG_LIGHT, LABEL_FG, 0.195, 0.14, "e", 18)
        name_label['font'] = font.Font(slant="italic", size=16)

        self.preset_preview.name = make_label(preset_preview_frame, "", MAIN_BG_LIGHT, LABEL_FG, 0.205, 0.14, "w", 18)

        description_label = make_label(preset_preview_frame, "Description:", MAIN_BG_LIGHT, LABEL_FG, 0.195, 0.21, "e", 18)
        description_label['font'] = font.Font(slant="italic", size=16)

        description_frame = make_frame(preset_preview_frame, "black", 0.77, 0.13, 0.205, 0.25, "w")
        self.preset_preview.description = make_text_box(description_frame, MAIN_BG_LIGHT, LABEL_FG, 12, 12)

        location_label = make_label(preset_preview_frame, "Sync Details:", MAIN_BG_LIGHT, LABEL_FG, 0.195, 0.43, "e", 18)
        location_label['font'] = font.Font(slant="italic", size=16)
        preview_tree_frame = make_frame(preset_preview_frame, MAIN_BG_LIGHT, 0.95, 0.4, 0.5, 0.67, "center")
        self.location_preview_tree = make_tree_view(preview_tree_frame, TREE_NAMES, TREE_WIDTHS)

        date_label = make_label(preset_preview_frame, "Date Created:", MAIN_BG_LIGHT, LABEL_FG, 0.195, 0.36, "e", 18)
        date_label['font'] = font.Font(slant="italic", size=16)
        self.preset_preview.date_created = make_label(preset_preview_frame, "", MAIN_BG_LIGHT, LABEL_FG, 0.205, 0.36, "w", 18)

        delete_button = make_button(preset_preview_frame, "Delete Preset", 1, 12, BUTTON_BG, "black", 0.5, 0.975, lambda: self.delete_confirm(preset_preview_frame), 16, "s")
        delete_button.config(bg=MAIN_BG_LIGHT)


    def _return_to_home(self, frame):
        frame.destroy()
        self.window.geometry(APP_DIMS_COMPACT)

    def _toggle_preset_details(self):
        if (self.window.winfo_width() == APP_EXPANDED_W) and (self.window.winfo_height() == APP_EXPANDED_H):
            self._set_window_compact()
        else:
            if self.presets.selected_preset is not None:
                self._set_window_expanded()
            else:
                self.notice_label.config(text="Select a preset first")

    def _set_window_compact(self):
        self.window.geometry(APP_DIMS_COMPACT)

    def _set_window_expanded(self):
        self.window.geometry(APP_DIMS_EXPANDED)

    def delete_confirm(self, preset_preview_frame):
        if self.presets.selected_preset is not None:
            confirm_button = make_button(preset_preview_frame, "Confirm Preset Deletion", 1, 20, BUTTON_BG, "black", 0.975, 0.975, None, 16, "se")
            confirm_button.config(command=lambda: self.remove_preset(confirm_button))
            confirm_button.config(bg="red")
        else:
            self.notice_label.config(text="Select a preset first")

    def remove_preset(self, confirm_button):
        self.presets.delete_preset(self.presets.selected_preset["name"])
        set_listbox(self.presets_listbox, self.presets.get_preset_names())
        self.presets.clear_selected_preset()
        self.preset_preview.clear_attributes()
        confirm_button.destroy()

    def create_preset_page(self):
        self._set_window_expanded()
        self.new_preset_locations = []
        create_preset_frame = make_frame(self.window, MAIN_BG, 1, 1, 0.5, 0.5, "center")
        make_button(create_preset_frame, "Cancel", 1, 6, BUTTON_BG, "black", 0.0125, 0.0125, lambda: self._return_to_manage(create_preset_frame), 16, "nw")
        make_label(create_preset_frame, "CREATE NEW PRESET", MAIN_BG, TITLE_FG, 0.5, 0.0125, "n", 20)

        name_lbl = make_label(create_preset_frame, "Name", MAIN_BG, LABEL_FG, 0.0125, 0.07, "nw", 18)
        name_lbl['font'] = font.Font(slant="italic", size=16)
        name_entry = make_entry(create_preset_frame, 64, ENTRY_BG, ENTRY_FG, "Preset "+str(datetime.now()), 0.0125, 0.1, "nw")

        desc_lbl = make_label(create_preset_frame, "Description", MAIN_BG, LABEL_FG, 0.0125, 0.14, "nw", 18)
        desc_lbl['font'] = font.Font(slant="italic", size=16)
        description_frame = make_frame(create_preset_frame, MAIN_BG, 0.97, 0.06, 0.0125, 0.17, "nw")
        description_entry = make_text_box(description_frame, ENTRY_BG, ENTRY_FG, 12, 12)

        locations_lbl = make_label(create_preset_frame, "Sync Locations", MAIN_BG, LABEL_FG, 0.0125, 0.24, "nw", 18)
        locations_lbl['font'] = font.Font(slant="italic", size=16)
        new_tree_frame = make_frame(create_preset_frame, ENTRY_BG, 1-.028, 0.3, 0.5, 0.27, "n")
        self.new_preset_tree = make_tree_view(new_tree_frame, TREE_NAMES, TREE_WIDTHS)

        main_notice = make_label(create_preset_frame, "", MAIN_BG_LIGHT, "red", 0.985, 0.065, "ne", 12)

        make_button(create_preset_frame, "Save", 1, 6, BUTTON_BG, "black", 1 - 0.0125, 0.0125, lambda: self._save_new_preset(main_notice, name_entry.get(), description_entry.get("1.0", tk.END), create_preset_frame), 16, "ne")

        self.add_sync_options(create_preset_frame)

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




    def add_folder_pair(self, folder_notice, src_entry, dst_entry, sub_folders_check, sync_files_edited, sync_deleted_files):
        if src_entry.get() != "":
            if dst_entry.get() != "":
                if src_entry.get() != dst_entry.get():

                    if sub_folders_check.get() == 1:
                        sub_folders_check = "Yes"
                    else:
                        sub_folders_check = "No"

                    if sync_files_edited.get() == 1:
                        sync_files_edited = "Yes"
                    else:
                        sync_files_edited = "No"

                    if sync_deleted_files.get() == 1:
                        sync_deleted_files = "Yes"
                    else:
                        sync_deleted_files = "No"

                    source = src_entry.get().replace('/', '//')
                    destination = dst_entry.get().replace('/', '//')

                    src_drive_name = get_drive_name(src_entry.get()[0])
                    dst_drive_name = get_drive_name(dst_entry.get()[0])

                    self.new_preset_locations.append((source, destination, sub_folders_check, sync_files_edited, sync_deleted_files, src_drive_name, dst_drive_name))
                    print(self.new_preset_locations)
                    set_tree_view(self.new_preset_tree, self.new_preset_locations)
                    src_entry.delete(0, tk.END)
                    dst_entry.delete(0, tk.END)

                else:
                    folder_notice.config(text="Source and Destination locations must be different")
            else:
                folder_notice.config(text="Select a Backup location")
        else:
            folder_notice.config(text="Select a Source location")



if __name__ == "__main__":
    root = tk.Tk()
    Window(root)
    root.mainloop()
