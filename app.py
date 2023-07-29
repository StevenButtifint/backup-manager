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
