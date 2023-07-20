import sys
import time
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import QThread, pyqtSignal

from res.operations import *
from res.constants import *


class CompareThread(QThread):
    finished = pyqtSignal(list, list)

    def __init__(self, location_one, location_two, check_subfolder_similarity):
        super().__init__()
        self.location_one = location_one
        self.location_two = location_two
        self.check_subfolder_similarity = check_subfolder_similarity

    def run(self):
        if self.check_subfolder_similarity:
            location_one_differences, location_two_differences = list_unique_located_items(self.location_one, self.location_two)
        else:
            location_one_differences, location_two_differences = list_unique_items(self.location_one, self.location_two)

        self.finished.emit(location_one_differences, location_two_differences)

