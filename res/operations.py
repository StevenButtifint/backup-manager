import win32api
import shutil
import os
from os import listdir
from os.path import isfile, join


def get_files_only(location):
    files = [f for f in listdir(location) if isfile(join(location, f))]
    return files


def check_file_modified(file_dir_a, file_dir_b):
    if os.path.getmtime(file_dir_a) == os.path.getmtime(file_dir_b):
        return False
    else:
        return True




def basic_copy(src, dst):
    shutil.copy2(src, dst)




def get_drive_name(letter):
    disk_name = win32api.GetVolumeInformation(letter+":\\")[0]
    if disk_name == "":
        name = letter
    else:
        name = letter + " - " + disk_name
    return name


def get_drive_names():
    drive_names = []
    occupied_letters = connected_drive_letters()
    for letter in occupied_letters:
        drive_names.append(get_drive_name(letter))
    return drive_names


