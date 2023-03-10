import win32api
import shutil
import os
from os import listdir
from os.path import isfile, join

from res.constants import *


def get_files_only(location):
    files = [f for f in listdir(location) if isfile(join(location, f))]
    return files


def check_file_modified(file_dir_a, file_dir_b):
    if os.path.getmtime(file_dir_a) == os.path.getmtime(file_dir_b):
        return False
    else:
        return True


def get_files_including_subfolders(location):
    base_len = len(location)+1
    res = []
    for (location, dir_names, file_names) in os.walk(location):
        for file_name in file_names:
            if len(location) > base_len:
                sub_location = location[base_len:]
                sub_location = sub_location.replace("\\", "//")

                res.append(sub_location + "//" + str(file_name))
            else:
                res.append(file_name)

    return res


def basic_copy(src, dst):
    shutil.copy2(src, dst)


def make_dir(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)


def delete_file(directory):
    os.remove(directory)


def clear_empty_folders(base, file_directory):
    sub_folders = file_directory.count('//')
    for x in range(1, sub_folders+1):
        sub_location = file_directory.rsplit('//', x)[0]
        try:
            os.rmdir(base + "//" + sub_location)
        except:
            pass  # folder not empty




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


def connected_drive_letters():
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    letters = []
    for drive in drives:
        letters.append(drive[0])
    return letters




def get_saved_presets():
    json_file = open(resource_path(PRESETS_DIR))
    json_str = json_file.read()
    json_data = json.loads(json_str)
    return json_data

