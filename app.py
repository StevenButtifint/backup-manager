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

        else:



        else:
        else:
        else:
        else:









        else:
        else:
        else:

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
