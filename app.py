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
