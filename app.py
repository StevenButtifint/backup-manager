from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *
import sys
import os

from res.constants import *
from res.operations import *
from res.preset_list_widget import *
from res.threads import CompareThread, ShowWaitingChanges, PerformPreset


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi(self.resource_path(INTERFACE_DIR), self)
        self.main_page_stack = self.findChild(QStackedWidget, 'main_page_stack')
        self.compare_page_stack = self.findChild(QStackedWidget, 'compare_page_stack')
        self.setup_environment()
        self.setup_interface()
        self.selected_preset = None
        self.waiting_changes_thread = None
        self.perform_preset_thread = None
        self.compare_thread = None
        self.bar_animation = None
        self.show()

    def setup_environment(self):
        self.ensure_local_presets_file()

    def setup_interface(self):
        self.switch_main_page('page_home', SIZE_COMPACT)
        self.switch_page(self.compare_page_stack, "loading_page")
        self.setup_buttons()
        self.set_notice_text('all_preset_notice', NO_NOTICE)
        self.set_last_used_date()

    def setup_buttons(self):
        # home page
        btn_recommended_presets = self.findChild(QToolButton, 'btn_recommended_presets')
        btn_recommended_presets.clicked.connect(lambda: self.view_recommended_presets())
        btn_select_preset = self.findChild(QToolButton, 'btn_select_preset')
        btn_select_preset.clicked.connect(lambda: self.view_all_presets())
        btn_new_preset = self.findChild(QToolButton, 'btn_new_preset')
        btn_new_preset.clicked.connect(lambda: self.switch_main_page('page_new_preset', SIZE_EXPANDED))
        btn_compare_folders = self.findChild(QToolButton, 'btn_compare_folders')
        btn_compare_folders.clicked.connect(lambda: self.switch_main_page('page_compare_folders', SIZE_COMPACT))

        # recommend preset page
        btn_recommended_back = self.findChild(QToolButton, 'btn_recommended_back')
        btn_recommended_back.clicked.connect(lambda: self.switch_main_page('page_home', SIZE_COMPACT))
        btn_recommended_details = self.findChild(QToolButton, 'btn_recommended_details')
        btn_recommended_details.clicked.connect(lambda: self.toggle_page_size('page_recommended_presets'))
        btn_recommended_use = self.findChild(QToolButton, 'btn_recommended_use')
        btn_recommended_use.clicked.connect(lambda: self.select_preset())

        btn_choose_delete_recommended = self.findChild(QToolButton, 'btn_choose_delete_recommended')
        btn_choose_delete_recommended.clicked.connect(lambda: self.enable_preset_delete_option_recommended())
        btn_confirm_delete_recommended = self.findChild(QToolButton, 'btn_confirm_delete_recommended')
        btn_confirm_delete_recommended.clicked.connect(lambda: self.remove_preset_from_recommended_list())
        btn_confirm_delete_recommended.hide()

        recommended_presets_list = self.findChild(QListWidget, 'recommended_presets_list')
        recommended_presets_list.itemClicked.connect(self.recommended_presets_item_clicked)
        self.recommended_presets_list = PresetList(recommended_presets_list)

        # select preset page
        btn_select_back = self.findChild(QToolButton, 'btn_select_back')
        btn_select_back.clicked.connect(lambda: self.switch_main_page('page_home', SIZE_COMPACT))
        all_presets_list = self.findChild(QListWidget, 'all_presets_list')
        all_presets_list.itemClicked.connect(self.all_presets_item_clicked)
        btn_all_details = self.findChild(QToolButton, 'btn_all_details')
        btn_all_details.clicked.connect(lambda: self.toggle_page_size('page_select_preset'))
        btn_all_use = self.findChild(QToolButton, 'btn_all_use')
        btn_all_use.clicked.connect(lambda: self.select_preset())
        btn_choose_delete = self.findChild(QToolButton, 'btn_choose_delete')
        btn_choose_delete.clicked.connect(lambda: self.enable_preset_delete_option())
        btn_confirm_delete = self.findChild(QToolButton, 'btn_confirm_delete')
        btn_confirm_delete.clicked.connect(lambda: self.remove_preset_from_all_list())
        btn_confirm_delete.hide()

        self.all_presets_list = PresetList(all_presets_list)

        # new preset page
        btn_new_back = self.findChild(QToolButton, 'btn_new_back')
        btn_new_back.clicked.connect(lambda: self.switch_main_page('page_home', SIZE_COMPACT))

        btn_src_location = self.findChild(QToolButton, 'btn_src_location')
        self.line_src_location = self.findChild(QLineEdit, 'line_src_location')
        btn_src_location.clicked.connect(lambda: self.select_folder(self.line_src_location))
        btn_dst_location = self.findChild(QToolButton, 'btn_dst_location')
        self.line_dst_location = self.findChild(QLineEdit, 'line_dst_location')
        btn_dst_location.clicked.connect(lambda: self.select_folder(self.line_dst_location))

        btn_clear_table = self.findChild(QToolButton, 'btn_clear_table')
        btn_clear_table.clicked.connect(lambda: self.clear_new_preset_locations())

        btn_add_location = self.findChild(QToolButton, 'btn_add_location')
        btn_add_location.clicked.connect(lambda: self.add_preset_location())

        btn_save_new_preset = self.findChild(QToolButton, 'btn_save_new_preset')
        btn_save_new_preset.clicked.connect(lambda: self.save_new_preset())

        # compare page
        btn_compare_back = self.findChild(QToolButton, 'btn_compare_back')
        btn_compare_back.clicked.connect(lambda: self.switch_main_page('page_home', SIZE_COMPACT))

        btn_compare_one = self.findChild(QToolButton, 'btn_compare_one')
        line_compare_one = self.findChild(QLineEdit, 'line_compare_one')
        btn_compare_one.clicked.connect(lambda: self.select_folder(line_compare_one))
        btn_compare_two = self.findChild(QToolButton, 'btn_compare_two')
        line_compare_two = self.findChild(QLineEdit, 'line_compare_two')
        btn_compare_two.clicked.connect(lambda: self.select_folder(line_compare_two))
        self.chk_subfolder_similarity = self.findChild(QCheckBox, 'chk_subfolder_similarity')
        self.btn_compare_locations = self.findChild(QToolButton, 'btn_compare_locations')
        self.btn_compare_locations.clicked.connect(lambda: self.get_location_differences(line_compare_one.text(), line_compare_two.text()))

        location_one_list = self.findChild(QListWidget, 'location_one_list')
        location_two_list = self.findChild(QListWidget, 'location_two_list')
        location_one_list.itemClicked.connect(lambda item: self.on_location_item_clicked(line_compare_one.text(), item.text()))
        location_two_list.itemClicked.connect(lambda item: self.on_location_item_clicked(line_compare_two.text(), item.text()))

        # use preset page
        btn_use_back = self.findChild(QToolButton, 'btn_use_back')
        btn_use_back.clicked.connect(lambda: self.back_home_from_use())
        btn_use_preset = self.findChild(QToolButton, 'btn_use_preset')
        btn_use_preset.clicked.connect(lambda: self.perform_preset())

    @staticmethod
    def ensure_local_presets_file():
        if not os.path.isfile(PRESETS_DIR):
            write_json_file(PRESETS_DIR, [])

    def back_home_from_use(self):
        self.switch_main_page('page_home', SIZE_COMPACT)
        lbl_use_status = self.findChild(QLabel, 'lbl_use_status')
        lbl_use_status.setText(SYNC_READY)

    def set_last_used_date(self):
        presets_list = read_json_file(PRESETS_DIR)
        most_recent_date = '00/00/0000'
        for preset in presets_list:
            most_recent_date = get_later_date(most_recent_date, preset['last-used'])
        lbl_last_used = self.findChild(QLabel, 'lbl_last_used')
        lbl_last_used.setText(f'Last Used: {most_recent_date}')

    def all_presets_item_clicked(self, item):
        item_name = item.text()
        self.disable_all_preset_delete_option()
        self.show_all_preset_notice(NO_NOTICE)
        self.selected_preset = get_preset(PRESETS_DIR, item_name)
        all_preset_selected_name = self.findChild(QLabel, 'all_preset_selected_name')
        all_preset_selected_name.setText(item_name)
        all_preset_selected_description = self.findChild(QLabel, 'all_preset_selected_description')
        all_preset_selected_description.setText(self.selected_preset['description'])
        all_preset_selected_created = self.findChild(QLabel, 'all_preset_selected_created')
        all_preset_selected_created.setText(self.selected_preset['created'])
        all_preset_selected_last_used = self.findChild(QLabel, 'all_preset_selected_last_used')
        all_preset_selected_last_used.setText(self.selected_preset['last-used'])
        self.clear_locations_table('all_preset_selected_table')
        for location in self.selected_preset['locations']:
            src_location, dst_location, sub_folders, modifications, deletions, _, _ = location
            self.add_location_to_table('all_preset_selected_table', src_location, dst_location, sub_folders, modifications, deletions)

    def recommended_presets_item_clicked(self, item):
        item_name = item.text()
        self.disable_recommended_preset_delete_option()
        self.show_recommended_preset_notice(NO_NOTICE)
        self.selected_preset = get_preset(PRESETS_DIR, item_name)
        recommended_preset_selected_name = self.findChild(QLabel, 'recommended_preset_selected_name')
        recommended_preset_selected_name.setText(item_name)
        recommended_preset_selected_description = self.findChild(QLabel, 'recommended_preset_selected_description')
        recommended_preset_selected_description.setText(self.selected_preset['description'])
        recommended_preset_selected_created = self.findChild(QLabel, 'recommended_preset_selected_created')
        recommended_preset_selected_created.setText(self.selected_preset['created'])
        recommended_preset_selected_last_used = self.findChild(QLabel, 'recommended_preset_selected_last_used')
        recommended_preset_selected_last_used.setText(self.selected_preset['last-used'])
        self.clear_locations_table('recommended_preset_selected_table')
        for location in self.selected_preset['locations']:
            src_location, dst_location, sub_folders, modifications, deletions, _, _ = location
            self.add_location_to_table('recommended_preset_selected_table', src_location, dst_location, sub_folders, modifications, deletions)

    @staticmethod
    def on_location_item_clicked(location, item):
        open_file_explorer(location + "/" + item)

    def toggle_page_size(self, current_page_name):
        current_height = self.window().frameGeometry().height()
        if current_height == SIZE_COMPACT[1] + 32:
            self.switch_main_page(current_page_name, SIZE_EXPANDED)
        else:
            self.switch_main_page(current_page_name, SIZE_COMPACT)

    def add_preset_location(self):
        src_location = self.line_src_location.text()
        dst_location = self.line_dst_location.text()

        new_location_chk_sub_folders = self.findChild(QCheckBox, 'chk_sub_folders')
        new_location_chk_modifications = self.findChild(QCheckBox, 'chk_modifications')
        new_location_chk_deletions = self.findChild(QCheckBox, 'chk_deletions')

        if new_location_chk_sub_folders.isChecked():
            sub_folders = "Yes"
        else:
            sub_folders = "No"

        if new_location_chk_modifications.isChecked():
            modifications = "Yes"
        else:
            modifications = "No"

        if new_location_chk_deletions.isChecked():
            deletions = "Yes"
        else:
            deletions = "No"

        if src_location == "":
            print("set a src location")
        elif dst_location == "":
            print("set a dst location")
        elif src_location == dst_location:
            print("Source and Destination locations must be different")
        else:
            self.add_location_to_table('tbl_locations_added', src_location, dst_location, sub_folders, modifications, deletions)
            self.reset_new_location_pair()

    def add_location_to_table(self, table_name, src_location, dst_location, sub_folders, modifications, deletions):
        tbl_locations_added = self.findChild(QTableWidget, table_name)
        new_row_index = tbl_locations_added.rowCount()
        tbl_locations_added.insertRow(new_row_index)
        tbl_locations_added.setItem(new_row_index, 0, QTableWidgetItem(str(src_location)))
        tbl_locations_added.setItem(new_row_index, 1, QTableWidgetItem(str(dst_location)))
        tbl_locations_added.setItem(new_row_index, 2, QTableWidgetItem(sub_folders))
        tbl_locations_added.setItem(new_row_index, 3, QTableWidgetItem(modifications))
        tbl_locations_added.setItem(new_row_index, 4, QTableWidgetItem(deletions))

    def reset_new_location_pair(self):
        self.line_src_location.setText("")
        self.line_dst_location.setText("")

    def clear_new_preset_locations(self):
        self.clear_locations_table('tbl_locations_added')

    def clear_all_presets_table(self):
        self.clear_locations_table('all_preset_selected_table')

    def clear_locations_table(self, table_name):
        tbl_locations_added = self.findChild(QTableWidget, table_name)
        while tbl_locations_added.rowCount() > 0:
            tbl_locations_added.removeRow(0)

    def save_new_preset(self):
        new_preset_name_line = self.findChild(QLineEdit, 'line_preset_name')
        name = only_letters_numbers(new_preset_name_line.text())
        new_preset_description_line = self.findChild(QLineEdit, 'line_preset_description')
        description = only_letters_numbers(new_preset_description_line.text())
        locations = self.get_new_table_locations()

        new_preset = {
            "name": name,
            "description": description,
            "created": get_today_date(),
            "last-used": "never",
            "locations": locations,
            "drives": get_preset_drive_names(locations)
        }

        self.add_preset_to_saved_presets(new_preset)
        self.clear_new_preset_page()
        self.switch_main_page('page_home', SIZE_COMPACT)

    def get_new_table_locations(self):
        tbl_locations_added = self.findChild(QTableWidget, 'tbl_locations_added')
        locations = []
        for row in range(tbl_locations_added.rowCount()):
            src_location = tbl_locations_added.item(row, 0).text()
            dst_location = tbl_locations_added.item(row, 1).text()
            subfolders = tbl_locations_added.item(row, 2).text()
            modified = tbl_locations_added.item(row, 3).text()
            deletions = tbl_locations_added.item(row, 4).text()
            src_drive_letter = tbl_locations_added.item(row, 0).text()[0]
            dst_drive_letter = tbl_locations_added.item(row, 1).text()[0]
            locations.append([src_location, dst_location, subfolders, modified, deletions, src_drive_letter, dst_drive_letter])
        return locations

    def clear_new_preset_page(self):
        new_preset_name_line = self.findChild(QLineEdit, 'line_preset_name')
        new_preset_name_line.setText("")
        new_preset_description_line = self.findChild(QLineEdit, 'line_preset_description')
        new_preset_description_line.setText("")
        self.clear_new_preset_locations()

    def add_preset_to_saved_presets(self, new_preset):
        self.ensure_local_presets_file()
        presets_list = read_json_file(PRESETS_DIR)
        presets_list.append(new_preset)
        write_json_file(PRESETS_DIR, presets_list)

    def enable_preset_delete_option(self):
        if self.selected_preset is not None:
            btn_confirm_delete = self.findChild(QToolButton, 'btn_confirm_delete')
            btn_confirm_delete.setEnabled(True)
            btn_confirm_delete.show()
        else:
            print("no preset selected")
            self.show_all_preset_notice(NO_PRESET_SELECTION)

    def enable_preset_delete_option_recommended(self):
        if self.selected_preset is not None:
            btn_confirm_delete = self.findChild(QToolButton, 'btn_confirm_delete_recommended')
            btn_confirm_delete.setEnabled(True)
            btn_confirm_delete.show()
        else:
            print("no preset selected")
            self.show_recommended_preset_notice(NO_PRESET_SELECTION)

    def disable_all_preset_delete_option(self):
        btn_confirm_delete = self.findChild(QToolButton, 'btn_confirm_delete')
        btn_confirm_delete.setEnabled(False)
        btn_confirm_delete.hide()

    def disable_recommended_preset_delete_option(self):
        btn_confirm_delete = self.findChild(QToolButton, 'btn_confirm_delete_recommended')
        btn_confirm_delete.setEnabled(False)
        btn_confirm_delete.hide()

    def remove_preset_from_all_list(self):
        self.delete_preset()
        self.refresh_all_presets_list()

    def remove_preset_from_recommended_list(self):
        self.delete_preset()
        self.refresh_recommended_presets_list()

    def delete_preset(self):
        self.ensure_local_presets_file()
        presets_list = read_json_file(PRESETS_DIR)
        updated_list = [preset for preset in presets_list if preset['name'] != self.selected_preset['name']]
        write_json_file(PRESETS_DIR, updated_list)

    def show_all_preset_notice(self, notice):
        self.set_notice_text('all_preset_notice', notice)

    def show_recommended_preset_notice(self, notice):
        self.set_notice_text('recommended_preset_notice', notice)

    def set_notice_text(self, notice_label, notice_text):
        notice = self.findChild(QLabel, notice_label)
        notice.setText(notice_text)

    @staticmethod
    def select_folder(line_edit):
        path = get_directory()
        line_edit.setText(path)

    def view_recommended_presets(self):
        self.refresh_recommended_presets_list()
        self.switch_main_page('page_recommended_presets', SIZE_COMPACT)

    def view_all_presets(self):
        self.refresh_all_presets_list()
        self.switch_main_page('page_select_preset', SIZE_COMPACT)

    def refresh_recommended_presets_list(self):
        json_data = read_json_file(PRESETS_DIR)
        recommended_preset_names = []
        current_connected_drives = connected_drive_letters()
        for x in range(len(json_data)):
            preset_drives = json_data[x]["drives"]
            if set(preset_drives).issubset(current_connected_drives):
                recommended_preset_names.append(json_data[x]["name"])
        self.recommended_presets_list.set_list(recommended_preset_names)
        self.clear_recommended_preset_preview()

    def clear_recommended_preset_preview(self):
        recommended_preset_selected_name = self.findChild(QLabel, 'recommended_preset_selected_name')
        recommended_preset_selected_name.setText('-')
        recommended_preset_selected_description = self.findChild(QLabel, 'recommended_preset_selected_description')
        recommended_preset_selected_description.setText('-')
        recommended_preset_selected_created = self.findChild(QLabel, 'recommended_preset_selected_created')
        recommended_preset_selected_created.setText('-')
        recommended_preset_selected_last_used = self.findChild(QLabel, 'recommended_preset_selected_last_used')
        recommended_preset_selected_last_used.setText('-')
        self.disable_recommended_preset_delete_option()
        self.clear_locations_table('recommended_preset_selected_table')

    def refresh_all_presets_list(self):
        json_data = read_json_file(PRESETS_DIR)
        preset_names = []
        for x in range(len(json_data)):
            preset_names.append(json_data[x]["name"])
        self.all_presets_list.set_list(preset_names)
        self.clear_select_preset_preview()

    def clear_select_preset_preview(self):
        all_preset_selected_name = self.findChild(QLabel, 'all_preset_selected_name')
        all_preset_selected_name.setText('-')
        all_preset_selected_description = self.findChild(QLabel, 'all_preset_selected_description')
        all_preset_selected_description.setText('-')
        all_preset_selected_created = self.findChild(QLabel, 'all_preset_selected_created')
        all_preset_selected_created.setText('-')
        all_preset_selected_last_used = self.findChild(QLabel, 'all_preset_selected_last_used')
        all_preset_selected_last_used.setText('-')
        self.disable_all_preset_delete_option()
        self.clear_locations_table('all_preset_selected_table')

    def switch_main_page(self, page_name, window_size):
        self.switch_page(self.main_page_stack, page_name)
        self.setFixedWidth(window_size[0])
        self.setFixedHeight(window_size[1])
        self.set_notice_text('all_preset_notice', NO_NOTICE)
        self.set_notice_text('recommended_preset_notice', NO_NOTICE)
        if page_name == 'page_home':
            self.selected_preset = None

    def switch_page(self, page_stack, page_name):
        page_stack.setCurrentWidget(self.findChild(QWidget, page_name))

    def get_location_differences(self, location_one, location_two):
        if (location_one == "") or (location_two == ""):
            print("select locations")
        if not folder_exists(location_one) or not folder_exists(location_two):
            print("locations could not be found")
        else:
            self.btn_compare_locations.setEnabled(False)
            self.switch_page(self.compare_page_stack, "loading_page")
            self.switch_main_page('page_compare_folders', SIZE_EXPANDED)
            self.compare_thread = CompareThread(str(location_one), str(location_two), self.chk_subfolder_similarity.isChecked())
            self.compare_thread.finished.connect(self.show_comparison)
            self.compare_thread.start()

    def show_comparison(self, list_one, list_two):
        self.update_location_lists(list_one, list_two)
        self.update_location_lists_count(len(list_one), len(list_two))
        self.switch_page(self.compare_page_stack, "results_page")
        self.btn_compare_locations.setEnabled(True)

    def update_location_lists(self, list_one, list_two):
        location_one_list = self.findChild(QListWidget, 'location_one_list')
        location_two_list = self.findChild(QListWidget, 'location_two_list')
        location_one_list.clear()
        location_two_list.clear()
        location_one_list.addItems(list_one)
        location_two_list.addItems(list_two)

    def update_location_lists_count(self, list_one_count, list_two_count):
        lbl_location_one_count = self.findChild(QLabel, 'lbl_location_one_count')
        lbl_location_two_count = self.findChild(QLabel, 'lbl_location_two_count')
        lbl_location_one_count.setText(str(list_one_count) + " Items")
        lbl_location_two_count.setText(str(list_two_count) + " Items")

    def select_preset(self):
        if self.selected_preset is None:
            self.show_all_preset_notice(NO_PRESET_SELECTION)
            self.show_recommended_preset_notice(NO_PRESET_SELECTION)
        else:
            use_progress_bar = self.findChild(QProgressBar, 'use_progress_bar')
            use_progress_bar.setValue(0)
            use_preset_name = self.findChild(QLabel, 'use_preset_name')
            use_preset_name.setText(self.selected_preset["name"])
            use_preset_last_used = self.findChild(QLabel, 'use_preset_last_used')
            use_preset_last_used.setText(self.selected_preset["last-used"])
            self.switch_main_page('page_use_preset', SIZE_COMPACT)
            lbl_changes_waiting = self.findChild(QLabel, 'lbl_changes_waiting')
            lbl_changes_waiting.setText("Calculating number of potential changes...")

            self.waiting_changes_thread = ShowWaitingChanges(self.selected_preset["locations"])
            self.waiting_changes_thread.finished.connect(self.show_waiting_changes)
            self.waiting_changes_thread.start()

    def show_waiting_changes(self, changes_count, notice):
        lbl_changes_waiting = self.findChild(QLabel, 'lbl_changes_waiting')
        if notice == NO_NOTICE:
            lbl_changes_waiting.setText(f'{changes_count} changes are waiting to be synced.')
        else:
            lbl_changes_waiting.setText(f'{notice}')

    def perform_preset(self):
        self.disable_perform_preset()
        self.perform_preset_thread = PerformPreset(self.selected_preset["locations"])
        self.perform_preset_thread.update_status.connect(self.update_preset_progress)
        self.perform_preset_thread.finished.connect(self.preset_sync_finished)
        self.perform_preset_thread.start()

    def disable_perform_preset(self):
        btn_use_preset = self.findChild(QToolButton, 'btn_use_preset')
        btn_use_preset.setText('SYNCING')
        btn_use_preset.setEnabled(False)

    def enable_perform_preset(self):
        btn_use_preset = self.findChild(QToolButton, 'btn_use_preset')
        btn_use_preset.setText('START')
        btn_use_preset.setEnabled(True)

    def update_preset_progress(self, status, percent):
        self.update_preset_bar(percent)
        self.update_preset_status(status)

    def preset_sync_finished(self, status, num_saved, num_updated, num_cleared):
        print("preset thread is done")
        print(" info: ", str(num_saved), str(num_updated), str(num_cleared))
        self.update_preset_status(status)
        self.enable_perform_preset()
        if status == SYNC_COMPLETED_SUCCESS:
            self.update_preset_bar(100)
            lbl_changes_waiting = self.findChild(QLabel, 'lbl_changes_waiting')

            if (num_saved + num_updated + num_cleared) > 0:
                saved_string = f'Saved {num_saved}, ' if num_saved > 0 else ""
                updated_string = f'Updated {num_updated}, ' if num_updated > 0 else ""
                cleared_string = f'Cleared {num_cleared}, ' if num_cleared > 0 else ""
                full_string = saved_string + updated_string + cleared_string
                lbl_changes_waiting.setText(f'Successfully synced files. \n[{full_string[:-2]}]')
                use_preset_last_used = self.findChild(QLabel, 'use_preset_last_used')
                use_preset_last_used.setText(get_today_date())
                self.update_preset_last_used()
                self.set_last_used_date()

            else:
                lbl_changes_waiting.setText(f'Locations were already synced.')

    def update_preset_last_used(self):
        presets_list = read_json_file(PRESETS_DIR)

        for preset in presets_list:
            if preset['name'] == self.selected_preset['name']:
                preset['last-used'] = get_today_date()

        write_json_file(PRESETS_DIR, presets_list)

    def update_preset_bar(self, percent):
        use_progress_bar = self.findChild(QProgressBar, 'use_progress_bar')
        if use_progress_bar.value() == 100:
            use_progress_bar.setValue(0)

        self.bar_animation = QPropertyAnimation(use_progress_bar, b"value")
        self.bar_animation.setEasingCurve(QEasingCurve.InCubic)
        self.bar_animation.setEndValue(percent)
        self.bar_animation.setDuration(200)
        self.bar_animation.start()

    def update_preset_status(self, status):
        lbl_use_status = self.findChild(QLabel, 'lbl_use_status')
        lbl_use_status.setText(status)

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
    app = QtWidgets.QApplication([])
    window = Window()
    sys.exit(app.exec_())
