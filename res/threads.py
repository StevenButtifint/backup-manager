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


class ShowWaitingChanges(QThread):
    finished = pyqtSignal(int, str)

    def __init__(self, locations):
        super().__init__()
        self.locations = locations
        self.notice = NO_NOTICE

    def run(self):
        waiting_changes_total = 0
        for location in self.locations:

            src_location = location[0]
            dst_location = location[1]
            subfolders_check = location[2]

            if folder_exists(src_location) and folder_exists(dst_location):
                if subfolders_check == "Yes":
                    location_one_differences, location_two_differences = list_unique_located_items(src_location, dst_location)
                else:
                    location_one_differences, location_two_differences = list_unique_items(src_location, dst_location)

                waiting_changes_total += len(location_one_differences) + len(location_two_differences)
            else:
                self.notice = NO_LOCATION

        self.finished.emit(waiting_changes_total, self.notice)


class PerformPreset(QThread):
    finished = pyqtSignal(str, int, int, int)
    update_status = pyqtSignal(str, int)

    def __init__(self, locations):
        super().__init__()
        self.locations = locations
        self.location_count = len(locations)
        self.status = SYNC_ACTIVE
        self.alerts = SYNC_COMPLETED_SUCCESS
        self.bar_progress = 0
        self.bar_increment = self.set_bar_increment()

    def set_bar_increment(self):
        return int(100 / (len(self.locations) + 1))

    def increment_bar_progress(self):
        self.bar_progress += int(self.bar_increment)

    def run(self):
        files_saved = 0
        files_updated = 0
        files_cleared = 0

        for index, location in enumerate(self.locations):
            self.increment_bar_progress()
            src_location, dst_location, sub_folders_check, sync_files_edited, sync_deleted_files, src_drive_name, dst_drive_name = location

            # for both file and folder sync the dst must exist
            if not folder_exists(dst_location):
                self.alerts = SYNC_LOCATIONS_SKIPPED
                print(dst_location, "dst directory does not exist.")

            # if src is dir that doesnt exist then don't sync for safety but notify user
            if not file_path(src_location) and not folder_exists(src_location):
                self.alerts = SYNC_LOCATIONS_SKIPPED
                print(src_location, "src directory does not exist.")

