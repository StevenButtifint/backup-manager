from datetime import datetime

from res.constants import *
from res.interface import *
from res.operations import *
from res.presets import Presets
from res.location_pair import LocationPair
from res.preset_preview import PresetPreview


class Window:
    def __init__(self, parent):
        self.window = parent
        self.window.title(APP_TITLE)
        self.window.resizable(False, False)
        self.window.geometry(APP_DIMS_COMPACT)
        self.window.iconbitmap(self.resource_path(APP_ICON_DIR))
        self.window.config(bg=MAIN_BG)
        self.presets = Presets(self.resource_path(""))
        self.preset_preview = PresetPreview()
        self.new_preset_locations = []
        self.notice_label = tk.Button()
        self.last_sync_label = tk.Label()
        self.presets_listbox = []
        self.location_preview_tree = []
        self.new_preset_tree = []
        self.previous_page = None
        self.home_page()

    def home_page(self):
        set_style()
        home_frame = make_frame(self.window, MAIN_BG, 1, 1, 0.5, 0.5, "center")
        make_label(home_frame, "WELCOME", MAIN_BG, TITLE_FG, 0.5, 0.01, "n", 22)
        make_img_button(home_frame, "Recommended\nPresets", 240, 200, BUTTON_BG, "black", 0, 0.5, "w", lambda: self.recommend_preset_page(), 14, self.resource_path(TICK_ICON_DIR))
        make_img_button(home_frame, "Select a\nPreset", 240, 200, BUTTON_BG, "black", 0.25, 0.5, "w", lambda: self.select_preset_page(), 14, self.resource_path(SEARCH_ICON_DIR))
        make_img_button(home_frame, "Create New\nPreset", 240, 200, BUTTON_BG, "black", 0.5, 0.5, "w", lambda: self.create_preset_page(), 14, self.resource_path(ADD_ICON_DIR))
        make_img_button(home_frame, "Compare\nFolders", 240, 200, BUTTON_BG, "black", 0.75, 0.5, "w", lambda: self.compare_locations_page(), 14, self.resource_path(COMPARE_ICON_DIR))
        make_label(home_frame, APP_VERSION, MAIN_BG, VERSION_FG, 1, 1, "se", 10)
        self.last_sync_label = make_label(home_frame, get_last_used_string(self.resource_path("")), MAIN_BG, UPDATED_FG, 0.5, 0.94, "c", 14)

    def recommend_preset_page(self):
        self.presets.update_recommended_presets()
        self.presets.clear_selected_preset()
        recommend_frame = make_static_frame(self.window, MAIN_BG, APP_EXPANDED_W, APP_EXPANDED_H, 400, 450, "center")
        make_label(recommend_frame, "RECOMMENDED PRESETS", MAIN_BG, TITLE_FG, 0.5, 0.005, "n", 22)
        make_back_button(recommend_frame, lambda: self._return_to_manage(recommend_frame), self.resource_path(BACK_ICON_DIR))
        presets_frame = make_frame(recommend_frame, MAIN_BG, 1, 0.27, 0.5, 0.049, "n")
        presets_listbox = make_listbox(presets_frame, 18, LISTBOX_BG, LISTBOX_FG)
        presets_listbox.bind('<<ListboxSelect>>', self.recommended_preset_selected)
        set_listbox(presets_listbox, self.presets.recommended_preset_names)
        make_button(recommend_frame, "Create New Preset", 1, 21, BUTTON_BG, "black", 0.0005, 0.3175, lambda: self.create_preset_page(), 16, "nw")
        preset_details = make_button(recommend_frame, "Toggle Preset Details", 1, 21, BUTTON_BG, "black", 0.5, 0.3175, lambda: None, 16, "n")
        preset_details.config(command=lambda: self._toggle_preset_details())
        make_button(recommend_frame, "Use Preset", 1, 21, BUTTON_BG, "black", 0.9995, 0.3175, lambda: self.operation_page(), 16, "ne")
        preset_preview_frame = make_frame(recommend_frame, MAIN_BG_LIGHT, 1, 0.63, 0.5, 1, "s")
        self._create_preset_preview(preset_preview_frame)
        self.notice_label = make_label(recommend_frame, "", MAIN_BG, "red", 1, 0.015, "ne", 12)
        self.previous_page = recommend_frame

    def select_preset_page(self):
        self.presets.clear_selected_preset()
        manage_preset_frame = make_static_frame(self.window, MAIN_BG, APP_EXPANDED_W, APP_EXPANDED_H, 400, 450, "center")
        make_label(manage_preset_frame, "SELECT PRESET", MAIN_BG, TITLE_FG, 0.5, 0.005, "n", 22)
        presets_frame = make_frame(manage_preset_frame, MAIN_BG, 1, 0.2675, 0.5, 0.049, "n")
        self.presets_listbox = make_listbox(presets_frame, 18, LISTBOX_BG, LISTBOX_FG)
        self.presets_listbox.bind('<<ListboxSelect>>', self.saved_preset_selected)
        set_listbox(self.presets_listbox, self.presets.get_preset_names())
        preset_details = make_button(manage_preset_frame, "Toggle Preset Details", 1, 21, BUTTON_BG, "black", 0.5, 0.3175, lambda: None, 16, "n")
        preset_details.config(command=lambda: self._toggle_preset_details())
        make_button(manage_preset_frame, "Create New Preset", 1, 21, BUTTON_BG, "black", 0.0005, 0.3175, lambda: self.create_preset_page(), 16, "nw")
        make_back_button(manage_preset_frame, lambda: self._return_to_manage(manage_preset_frame), self.resource_path(BACK_ICON_DIR))
        make_button(manage_preset_frame, "Use Preset", 1, 21, BUTTON_BG, "black", 0.9995, 0.3175, lambda: self.operation_page(), 16, "ne")
        self.notice_label = make_label(manage_preset_frame, "", MAIN_BG, "red", 0.975, 0.015, "ne", 12)
        preset_preview_frame = make_frame(manage_preset_frame, MAIN_BG_LIGHT, 1, 0.63, 0.5, 1, "s")
        self._create_preset_preview(preset_preview_frame)
        self.previous_page = manage_preset_frame

    def _create_preset_preview(self, frame):
        make_label(frame, "PRESET DETAILS", MAIN_BG_LIGHT, LISTBOX_BG, 0.5, 0.09, "s", 20)
        name_label = make_label(frame, "Name", MAIN_BG_LIGHT, LISTBOX_BG, 0.02, 0.1, "w", 18)
        name_label['font'] = font.Font(slant="italic", size=16)
        self.preset_preview.name = make_label(frame, "", MAIN_BG_LIGHT, PREVIEW_FG, 0.02, 0.15, "w", 18)
        description_label = make_label(frame, "Description", MAIN_BG_LIGHT, LISTBOX_BG, 0.02, 0.21, "w", 18)
        description_label['font'] = font.Font(slant="italic", size=16)
        description_frame = make_frame(frame, "black", 0.958, 0.14, 0.022, 0.31, "w")
        self.preset_preview.description = make_text_box(description_frame, MAIN_BG_LIGHT, PREVIEW_FG, 12, 12)
        location_label = make_label(frame, "Sync Details", MAIN_BG_LIGHT, LISTBOX_BG, 0.02, 0.43, "w", 18)
        location_label['font'] = font.Font(slant="italic", size=16)
        preview_tree_frame = make_frame(frame, MAIN_BG_LIGHT, 0.95, 0.4, 0.5, 0.67, "center")
        self.location_preview_tree = make_tree_view(preview_tree_frame, TREE_NAMES, TREE_WIDTHS)
        date_label = make_label(frame, "Date Created", MAIN_BG_LIGHT, LISTBOX_BG, 0.65, 0.43, "w", 18)
        date_label['font'] = font.Font(slant="italic", size=16)
        self.preset_preview.date_created = make_label(frame, "", MAIN_BG_LIGHT, PREVIEW_FG, 0.98, 0.43, "e", 18)
        delete_button = make_button(frame, "Delete Preset", 1, 12, BUTTON_BG, "black", 0.5, 0.99, lambda: self.delete_confirm(frame), 16, "s")
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
            confirm_button = make_button(preset_preview_frame, "Confirm Preset Deletion", 1, 20, BUTTON_BG, "black", 0.99, 0.99, None, 16, "se")
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
        make_back_button(create_preset_frame, lambda: self._return_to_manage(create_preset_frame), self.resource_path(BACK_ICON_DIR))
        make_label(create_preset_frame, "CREATE NEW PRESET", MAIN_BG, TITLE_FG, 0.5, 0.005, "n", 22)

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

        main_notice = make_label(create_preset_frame, "", MAIN_BG, "red", 0.985, 0.065, "ne", 12)
        make_button(create_preset_frame, "Save Preset", 1, 64, BUTTON_BG, "black", 0.5, 0.99, lambda: self._save_new_preset(main_notice, name_entry.get(), description_entry.get("1.0", tk.END), create_preset_frame), 16, "s")
        self.add_sync_options(create_preset_frame)
        self.previous_page = create_preset_frame

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
        folder_pair = LocationPair(add_folder_tab, "Set Source Folder", add_folder)
        _, sub_folders_check = make_checkbutton(add_folder_tab, "Include Source Sub Folders", 16, TAB_BG_SELECTED, None, 0.01, 0.5, "w")
        _, sync_files_edited = make_checkbutton(add_folder_tab, "Sync File Alterations ", 16, TAB_BG_SELECTED, None, 0.01, 0.65, "w")
        _, sync_deleted_files = make_checkbutton(add_folder_tab, "Sync Deleted Files", 16, TAB_BG_SELECTED, None, 0.01, 0.8, "w")
        folder_notice = make_label(add_folder_tab, "", TAB_BG_SELECTED, "red", 0.74, 0.86, "ne", 12)
        make_button(add_folder_tab, "Add Location Pair", 1, 14, BUTTON_BG, "black", 0.99, 0.97, lambda: self.add_folder_pair(folder_notice, folder_pair, sub_folders_check, sync_files_edited, sync_deleted_files), 16, "se")

        # add file things
        add_file_tab = make_frame(tabs[1], TAB_BG_SELECTED, 1, 1, 0.5, 0.5, "center")
        _, sync_file_edited = make_checkbutton(add_file_tab, "Sync File Alterations ", 16, TAB_BG_SELECTED, None, 0.01, 0.5, "w")
        _, sync_file_deleted = make_checkbutton(add_file_tab, "Sync Deleted Files", 16, TAB_BG_SELECTED, None, 0.01, 0.65, "w")
        file_pair = LocationPair(add_file_tab,  "Set Source File", add_file)
        file_notice = make_label(add_file_tab, "", TAB_BG_SELECTED, "red", 0.74, 0.86, "ne", 12)
        make_button(add_file_tab, "Add Location Pair", 1, 14, BUTTON_BG, "black", 0.99, 0.97, lambda: self.add_file_pair(file_notice, file_pair, sync_file_edited, sync_file_deleted), 16, "se")

    def add_file_pair(self, file_notice, file_pair, sync_edited, sync_deleted):
        if file_pair.valid_src():
            if file_pair.valid_dst():
                if file_pair.dst_entry.get() not in file_pair.src_entry.get():
                    source = file_pair.src_entry.get().replace('/', '//')
                    destination = file_pair.dst_entry.get().replace('/', '//')

                    src_drive_name = get_drive_name(file_pair.src_entry.get()[0])
                    dst_drive_name = get_drive_name(file_pair.dst_entry.get()[0])

                    self.new_preset_locations.append((source, destination, "No", sync_edited.get(), sync_deleted.get(), src_drive_name, dst_drive_name))
                    set_tree_view(self.new_preset_tree, self.new_preset_locations)
                    file_pair.clear_entries()
                else:
                    file_notice.config(text="Source and Destination locations must be different")
            else:
                file_notice.config(text="Select a Backup location")
        else:
            file_notice.config(text="Select a Source location")

    def add_folder_pair(self, folder_notice, folder_pair, sub_folders_check, sync_files_edited, sync_deleted_files):
        if folder_pair.valid_src():
            if folder_pair.valid_dst():
                if folder_pair.valid_pair():
                    source = folder_pair.src_entry.get().replace('/', '//')
                    destination = folder_pair.dst_entry.get().replace('/', '//')

                    src_drive_name = get_drive_name(folder_pair.src_entry.get()[0])
                    dst_drive_name = get_drive_name(folder_pair.dst_entry.get()[0])

                    self.new_preset_locations.append((source, destination, sub_folders_check.get(), sync_files_edited.get(), sync_deleted_files.get(), src_drive_name, dst_drive_name))
                    set_tree_view(self.new_preset_tree, self.new_preset_locations)
                    folder_pair.clear_entries()
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
            self.sync_back_button = make_img_button(operation_page_frame, "", 36, 60, BUTTON_BG, "black", 0.000, 0.000, "nw", lambda: self._return_to_manage(operation_page_frame), 16, self.resource_path(BACK_ICON_DIR))

            make_label(operation_page_frame, "SYNC PRESET", MAIN_BG, TITLE_FG, 0.5, 0.001, "n", 22)

            info_frame = make_frame(operation_page_frame, LISTBOX_BG, 1, 0.68, 0.5, 0.465, "center")

            name_label = make_label(info_frame, "Name", MAIN_BG, LISTBOX_BG, 0.5, 0.25, "c", 16)
            name_label['font'] = font.Font(slant="italic")

            saved = make_img(info_frame, "0 Saved", 160, 160, LISTBOX_BG, "black", 0.25, 0.55, "c", 14, self.resource_path(DOWNLOAD_ICON_DIR))
            updated = make_img(info_frame, "0 Updated", 200, 200, LISTBOX_BG, "black", 0.5, 0.55, "c", 14, self.resource_path(RELOAD_ICON_DIR))
            cleared = make_img(info_frame, "0 Cleared", 200, 200, LISTBOX_BG, "black", 0.75, 0.55, "c", 14, self.resource_path(UPLOAD_ICON_DIR))

            results = saved, updated, cleared

            make_label(info_frame, "Preset: "+self.presets.selected_preset["name"], LISTBOX_BG, "black", 0.5, 0.1, "c", 17)


            status = make_label(operation_page_frame, "Ready", MAIN_BG, LISTBOX_BG, 0.01, 0.93, "sw", 16)
            bar_progress = make_progress_bar(operation_page_frame, 0.5, 1, 800, "s")

            start_button = make_button(operation_page_frame, "START", 1, 14, BUTTON_BG, "black", 1, 0.9465, lambda: None, 16, "se")
            self.bar_progress = bar_progress
            self.status = status
            self.start_button = start_button
            self.results = results
            start_button.config(command=self.setup_preset_thread)

        else:
            self.notice_label.config(text="Select a preset to continue")

    def update_results(self, saved, updated, cleared):
        self.results[0].config(text=str(saved) + " Saved")
        self.results[1].config(text=str(updated) + " Updated")
        self.results[2].config(text=str(cleared) + " Cleared")

    def setup_preset_thread(self):
        self.start_button.configure(state="disabled")
        self.sync_back_button.configure(state="disabled")
        thread = threading.Thread(target=self.perform_preset_thread)
        thread.start()

    def perform_preset(self, bar_progress, status, start_button, results):####old
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
        self.preset_preview.set_name(self.presets.selected_preset["name"])
        self.preset_preview.set_description(self.presets.selected_preset["description"])
        self.preset_preview.set_date_created(self.presets.selected_preset["created"])
        set_tree_view(self.location_preview_tree, self.presets.selected_preset["locations"])
        self.notice_label.config(text="")

    def saved_preset_selected(self, event):
        w = event.widget
        index = int(w.curselection()[0])
        self.presets.selected_preset = self.presets.saved_presets[index]
        self.preset_preview.set_name(self.presets.selected_preset["name"])
        self.preset_preview.set_description(self.presets.selected_preset["description"])
        self.preset_preview.set_date_created(self.presets.selected_preset["created"])
        set_tree_view(self.location_preview_tree, self.presets.selected_preset["locations"])
        self.notice_label.config(text="")

    def compare_locations_page(self):
        compare_locations_frame = make_static_frame(self.window, MAIN_BG, APP_EXPANDED_W, APP_EXPANDED_H, 400, 450, "center")
        make_back_button(compare_locations_frame, lambda: self._return_to_manage(compare_locations_frame), self.resource_path(BACK_ICON_DIR))

        make_label(compare_locations_frame, "COMPARE LOCATIONS", MAIN_BG, TITLE_FG, 0.5, 0.005, "n", 22)
        make_label(compare_locations_frame, "Compare the difference between two folders contents.", MAIN_BG, TITLE_FAINT_FG, 0.5, 0.08, "c", 14)

        name_lbl = make_label(compare_locations_frame, "Location One", MAIN_BG, LABEL_FAINT_FG, 0.0125, 0.11, "nw", 14)
        name_lbl['font'] = font.Font(slant="italic", size=14)
        name_lbl = make_label(compare_locations_frame, "Location Two", MAIN_BG, LABEL_FAINT_FG, 0.0125, 0.18, "nw", 14)
        name_lbl['font'] = font.Font(slant="italic", size=14)

        make_label(compare_locations_frame, "Compare location similarity of files in subfolders.\t\t\t        \n"
                                            " e.g. The same file in different subfolder locations will be shown as a difference.", MAIN_BG, TITLE_FAINT_FG, 0.55, 0.28, "c", 12)

        make_label(compare_locations_frame, "_"*23+" "*50+"_"*23, MAIN_BG, LABEL_FAINT_FG, 0.5, 0.32, "c", 14)


    def compare_folders(self, use_location_similarity, entry_one, entry_two, listbox_one, listbox_two, loc_one_count, loc_two_count, notice):
        location_one = entry_one.get()
        location_two = entry_two.get()
        notice.config(text="")

        if folder_exists(location_one) and folder_exists(location_two):
            if use_location_similarity == "Yes":
                unique_loc_one, unique_loc_two = list_unique_located_items(location_one, location_two)
            else:
                unique_loc_one, unique_loc_two = list_unique_items(location_one, location_two)
            set_listbox(listbox_one, unique_loc_one)
            set_listbox(listbox_two, unique_loc_two)
            loc_one_count.config(text=str(len(unique_loc_one))+" Items")
            loc_two_count.config(text=str(len(unique_loc_two))+" Items")
            self._set_window_expanded()
        else:
            notice.config(text="Locations not found")
            self._set_window_compact()

    @staticmethod
    def resource_path(relative_path):
        # Get absolute path to resource, works for dev and for PyInstaller
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    root = tk.Tk()
    Window(root)
    root.mainloop()
