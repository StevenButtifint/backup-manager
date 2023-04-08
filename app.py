from datetime import datetime

from res.constants import *
from res.interface import *
from res.operations import *
from res.presets import Presets
from res.preset_preview import PresetPreview


class Window:
    def __init__(self, parent):
        self.window = parent
        self.window.title(APP_TITLE)
        self.window.resizable(False, False)
        self.window.geometry(APP_DIMS_COMPACT)
        self.window.iconbitmap(APP_ICON_DIR)
        self.window.config(bg=MAIN_BG)
        self.presets = Presets()
        self.preset_preview = PresetPreview()
        self.new_preset_locations = []
        self.notice_label = tk.Button()
        self.presets_listbox = []
        self.location_preview_tree = []
        self.new_preset_tree = []
        self.previous_page = None
        self.home_page()

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
        presets_listbox.bind('<<ListboxSelect>>', self.recommended_preset_selected)
        set_listbox(presets_listbox, self.presets.recommended_preset_names)
        make_button(recommend_frame, "Confirm", 1, 14, BUTTON_BG, "black", 0.9865, 0.31, lambda: self.operation_page(), 16, "ne")
        self.notice_label = make_label(recommend_frame, "", MAIN_BG_LIGHT, "red", 0.975, 0.025, "ne", 12)
        self.previous_page = recommend_frame

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
        make_button(manage_preset_frame, "Confirm", 1, 14, BUTTON_BG, "black", 0.9865, 0.31, lambda: self.operation_page(), 16, "ne")
        self.notice_label = make_label(manage_preset_frame, "", MAIN_BG_LIGHT, "red", 0.975, 0.025, "ne", 12)

        preset_preview_frame = make_frame(manage_preset_frame, MAIN_BG_LIGHT, 1, 0.63, 0.5, 1, "s")
        make_label(preset_preview_frame, "PRESET DETAILS", MAIN_BG_LIGHT, LABEL_FG, 0.5, 0.09, "s", 20)

        name_label = make_label(preset_preview_frame, "Name", MAIN_BG_LIGHT, LISTBOX_BG, 0.02, 0.1, "w", 18)
        name_label['font'] = font.Font(slant="italic", size=16)

        self.preset_preview.name = make_label(preset_preview_frame, "", MAIN_BG_LIGHT, PREVIEW_FG, 0.02, 0.15, "w", 18)

        description_label = make_label(preset_preview_frame, "Description", MAIN_BG_LIGHT, LISTBOX_BG, 0.02, 0.21, "w", 18)
        description_label['font'] = font.Font(slant="italic", size=16)

        description_frame = make_frame(preset_preview_frame, "black", 0.958, 0.14, 0.022, 0.31, "w")
        self.preset_preview.description = make_text_box(description_frame, MAIN_BG_LIGHT, PREVIEW_FG, 12, 12)

        location_label = make_label(preset_preview_frame, "Sync Details", MAIN_BG_LIGHT, LISTBOX_BG, 0.02, 0.43, "w", 18)
        location_label['font'] = font.Font(slant="italic", size=16)
        preview_tree_frame = make_frame(preset_preview_frame, MAIN_BG_LIGHT, 0.95, 0.4, 0.5, 0.67, "center")
        self.location_preview_tree = make_tree_view(preview_tree_frame, TREE_NAMES, TREE_WIDTHS)

        date_label = make_label(preset_preview_frame, "Date Created", MAIN_BG_LIGHT, LISTBOX_BG, 0.65, 0.43, "w", 18)
        date_label['font'] = font.Font(slant="italic", size=16)
        self.preset_preview.date_created = make_label(preset_preview_frame, "", MAIN_BG_LIGHT, PREVIEW_FG, 0.98, 0.43, "e", 18)

        delete_button = make_button(preset_preview_frame, "Delete Preset", 1, 12, BUTTON_BG, "black", 0.5, 0.99, lambda: self.delete_confirm(preset_preview_frame), 16, "s")
        delete_button.config(bg=MAIN_BG_LIGHT)

        self.previous_page = manage_preset_frame

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
            self.previous_page.destroy()
            create_preset_frame.destroy()
            self._set_window_compact()

    def _return_to_manage(self, frame):
        frame.destroy()
        self._set_window_compact()

    def add_sync_options(self, frame):
        sub_options_frame = make_frame(frame, MAIN_BG, 1-.028, 0.35, 0.5, 0.58, "n")

        tabs = ["Add Folder Location", "Add File Location"]
        notebook, tabs = make_notebook(sub_options_frame, tabs, NOTEBOOK_BG, NOTEBOOK_FG)

        add_folder_tab = make_frame(tabs[0], TAB_BG_SELECTED, 1, 1, 0.5, 0.5, "center")

        # src_label = make_label(sub_options_frame, "", MAIN_BG_LIGHT, "black", 0.765, 0.05, "ne", 12)
        src_entry = make_entry(add_folder_tab, 42, ENTRY_BG, ENTRY_FG, "", 0.01, 0.08, "nw")

        # dst_label = make_label(sub_options_frame, "", MAIN_BG_LIGHT, "black", 0.765, 0.3, "ne", 12)
        dst_entry = make_entry(add_folder_tab, 42, ENTRY_BG, ENTRY_FG, "", 0.01, 0.28, "nw")

        make_button(add_folder_tab, "Set Source Folder", 1, 18, BUTTON_BG, "black", 0.99, 0.05, lambda: add_folder(src_entry), 16, "ne")
        make_button(add_folder_tab, "Set Backup Location", 1, 18, BUTTON_BG, "black", 0.99, 0.25, lambda: add_folder(dst_entry), 16, "ne")

        _, sub_folders_check = make_checkbutton(add_folder_tab, "Include Source Sub Folders", 16, TAB_BG_SELECTED, None, 0.01, 0.5, "w")
        _, sync_files_edited = make_checkbutton(add_folder_tab, "Sync File Alterations ", 16, TAB_BG_SELECTED, None, 0.01, 0.65, "w")
        _, sync_deleted_files = make_checkbutton(add_folder_tab, "Sync Deleted Files", 16, TAB_BG_SELECTED, None, 0.01, 0.8, "w")

        folder_notice = make_label(add_folder_tab, "", MAIN_BG_LIGHT, "red", 0.74, 0.86, "ne", 12)

        make_button(add_folder_tab, "Add Location Pair", 1, 14, BUTTON_BG, "black", 0.99, 0.97, lambda: self.add_folder_pair(folder_notice, src_entry, dst_entry, sub_folders_check, sync_files_edited, sync_deleted_files), 16, "se")

        # add file things
        add_file_tab = make_frame(tabs[1], TAB_BG_SELECTED, 1, 1, 0.5, 0.5, "center")

        _, sync_file_edited = make_checkbutton(add_file_tab, "Sync File Alterations ", 16, TAB_BG_SELECTED, None, 0.01, 0.5, "w")
        _, sync_file_deleted = make_checkbutton(add_file_tab, "Sync Deleted Files", 16, TAB_BG_SELECTED, None, 0.01, 0.65, "w")

        src_file_entry = make_entry(add_file_tab, 42, ENTRY_BG, ENTRY_FG, "", 0.01, 0.08, "nw")
        dst_file_entry = make_entry(add_file_tab, 42, ENTRY_BG, ENTRY_FG, "", 0.01, 0.28, "nw")

        make_button(add_file_tab, "Set Source File", 1, 18, BUTTON_BG, "black", 0.99, 0.05, lambda: add_file(src_file_entry), 16, "ne")
        make_button(add_file_tab, "Set Backup Location", 1, 18, BUTTON_BG, "black", 0.99, 0.25, lambda: add_folder(dst_file_entry), 16, "ne")

        file_notice = make_label(add_file_tab, "", MAIN_BG_LIGHT, "red", 0.74, 0.86, "ne", 12)

        make_button(add_file_tab, "Add Location Pair", 1, 14, BUTTON_BG, "black", 0.99, 0.97, lambda: self.add_file_pair(file_notice, src_file_entry, dst_file_entry, sync_file_edited, sync_file_deleted), 16, "se")

    def add_file_pair(self, file_notice, src_entry, dst_entry, sync_edited, sync_deleted):
        if src_entry.get() != "":
            if dst_entry.get() != "":
                if dst_entry.get() not in src_entry.get():
                    if sync_edited.get() == 1:
                        sync_edited = "Yes"
                    else:
                        sync_edited = "No"

                    if sync_deleted.get() == 1:
                        sync_deleted = "Yes"
                    else:
                        sync_deleted = "No"

                    source = src_entry.get().replace('/', '//')
                    destination = dst_entry.get().replace('/', '//')

                    src_drive_name = get_drive_name(src_entry.get()[0])
                    dst_drive_name = get_drive_name(dst_entry.get()[0])

                    self.new_preset_locations.append((source, destination, "No", sync_edited, sync_deleted, src_drive_name, dst_drive_name))
                    set_tree_view(self.new_preset_tree, self.new_preset_locations)
                    src_entry.delete(0, tk.END)
                    dst_entry.delete(0, tk.END)
                else:
                    file_notice.config(text="Source and Destination locations must be different")
            else:
                file_notice.config(text="Select a Backup location")
        else:
            file_notice.config(text="Select a Source location")

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
                    set_tree_view(self.new_preset_tree, self.new_preset_locations)
                    src_entry.delete(0, tk.END)
                    dst_entry.delete(0, tk.END)

                else:
                    folder_notice.config(text="Source and Destination locations must be different")
            else:
                folder_notice.config(text="Select a Backup location")
        else:
            folder_notice.config(text="Select a Source location")

    def operation_page(self):
        if self.presets.selected_preset is not None:
            self._set_window_compact()
            operation_page_frame = make_frame(self.window, MAIN_BG, 1, 1, 0.5, 0.5, "center")
            make_button(operation_page_frame, "Back", 1, 6, BUTTON_BG, "black", 0.0125, 0.033, lambda: operation_page_frame.destroy(), 16, "nw")

            make_label(operation_page_frame, "SYNC PRESET", MAIN_BG, TITLE_FG, 0.5, 0.036, "n", 20)

            make_label(operation_page_frame, "Preset:  " + self.presets.selected_preset["name"], MAIN_BG, "white", 0.2, 0.3, "w", 17)

            results = make_label(operation_page_frame, "Details:  Results will be shown here.", MAIN_BG, "white", 0.2, 0.45, "w", 17)


            status = make_label(operation_page_frame, "Ready", MAIN_BG, "grey", 0.01, 0.91, "sw", 16)
            bar_progress = make_progress_bar(operation_page_frame, 0.5, 0.98, 780, "s")

            start_button = make_button(operation_page_frame, "Start", 1, 6, BUTTON_BG, "black", 0.9865, 0.88, lambda: None, 16, "se")
            start_button.config(command=lambda: self.perform_preset(bar_progress, status, operation_page_frame, start_button, results))

        else:
            self.notice_label.config(text="Select a preset to continue")

    def perform_preset(self, bar_progress, status, operation_page_frame, start_button, results):
        start_button.destroy()
        operation_count = len(self.presets.selected_preset["locations"])
        bar_increment = int(100/operation_count)

        files_saved = 0
        files_updated = 0
        files_cleared = 0

        count = 1
        for location in self.presets.selected_preset["locations"]:
            print("Processing: " + str(location))

            # currently assume:
            # -locations exist and use same drive letters as when created

            src_location, dst_location, sub_folders_check, sync_files_edited, sync_deleted_files, src_drive_name, dst_drive_name = location

            # get list of files in src location (without src location prefix)
            if sub_folders_check == "Yes":
                current_files = get_files_including_subfolders(src_location)
            else:
                current_files = get_files_only(src_location)
            print("\tSRC items:" + str(current_files))

            # get list of files in dst location (without dst location prefix)
            current_files_save = get_files_including_subfolders(dst_location)
            print("\tDST items:" + str(current_files_save))

            # if sync_deleted_files do this
            if sync_deleted_files == "Yes":
                for file in current_files_save:
                    if file not in current_files:
                        print("\t\tDELETED FILE (delete): "+str(file) + " (should be deleted from backup)")
                        delete_file(dst_location+"//"+file)
                        clear_empty_folders(dst_location, file)
                        files_cleared += 1

            # check modified files
            if sync_files_edited == "Yes":
                for file in current_files_save:
                    if file in current_files:
                        if check_file_modified(src_location+"//"+file, dst_location+"//"+file):
                            print("\t\tEDITED FILE (save): " + str(file) + " (should be copied to replace old backup version)")
                            # use basic copy as should overwrite file in dst location but needs to be tested
                            if "//" in file:
                                sub_location = file.rsplit('//', 1)
                                sub_location = sub_location[0]
                                make_dir(dst_location + "//" + sub_location)
                            basic_copy(src_location + "//" + file, dst_location + "//" + file)
                            files_updated += 1

                            # sync new files
            for file in current_files:
                if file not in current_files_save:
                    print("\t\tNEW FILE (save): " + file)  # note: save to sub location in dst if in sub location in src
                    if "//" in file:
                        sub_location = file.rsplit('//', 1)
                        sub_location = sub_location[0]
                        make_dir(dst_location+"//"+sub_location)
                    basic_copy(src_location+"//"+file, dst_location+"//"+file)
                    files_saved += 1

            status.config(text="Processing ("+str(count)+"/"+str(operation_count)+")")
            count += 1
            bar_progress.config(value=bar_progress["value"]+bar_increment)
            self.window.update_idletasks()

            import time
            time.sleep(1)

        results.config(text="Details:  Saved: "+str(files_saved)+"    Updated: "+str(files_updated)+"    Cleared: "+str(files_cleared))
        status.config(text="Completed")
        make_button(operation_page_frame, "Close", 1, 6, BUTTON_BG, "black", 0.9865, 0.88, lambda: operation_page_frame.destroy(), 16, "se")

    def recommended_preset_selected(self, event):
        w = event.widget
        index = int(w.curselection()[0])
        self.presets.set_selected_preset(self.presets.recommended_presets[index])

    def saved_preset_selected(self, event):
        w = event.widget
        index = int(w.curselection()[0])
        self.presets.selected_preset = self.presets.saved_presets[index]
        self.preset_preview.set_name(self.presets.selected_preset["name"])
        self.preset_preview.set_description(self.presets.selected_preset["description"])
        self.preset_preview.set_date_created(self.presets.selected_preset["created"])
        set_tree_view(self.location_preview_tree, self.presets.selected_preset["locations"])
        self.notice_label.config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    Window(root)
    root.mainloop()
