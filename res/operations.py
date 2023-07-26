import subprocess
import win32api
import shutil
import json
import os
import re

from tkinter.filedialog import askdirectory, askopenfilename
from PyQt5.QtWidgets import *
from datetime import datetime, date
from os.path import isfile, join
from os import listdir

from res.constants import *


def get_directory():
    path = QFileDialog.getExistingDirectory(caption='Select a Folder')
    return path


def get_today_date():
    return datetime.today().strftime('%d/%m/%y')


def get_later_date(date_one, date_two):
    if date_one == 'never':
        date_one = date_two
    if date_two == 'never':
        date_two = date_one
    return max(date_one, date_two)


def open_file_explorer(location):
    location = location.replace('//', '\\')
    location = location.replace('/', '\\')
    subprocess.Popen(r'explorer /select,"'+location+'"')


def only_letters_numbers(raw_string):
    sanitized_string = re.sub(r'[^A-Za-z0-9 ]+', '', str(raw_string))
    return sanitized_string


def get_files_only(location):
    files = [f for f in listdir(location) if isfile(join(location, f))]
    return files


def get_file_only(location):
    if os.path.exists(location):
        return [location.split("//")[-1]]
    else:
        return []


def get_file_folder(location):
    return '//'.join(location.split('//')[0:-1])


def get_modified_time(directory):
    try:
        return os.path.getmtime(directory)
    except FileNotFoundError:
        return None


def check_file_modified(file_dir_a, file_dir_b):
    try:
        return os.path.getmtime(file_dir_a) != os.path.getmtime(file_dir_b)
    except FileNotFoundError:
        return False


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


def get_folder():
    path = askdirectory(title='Select Folder')
    print(path)
    return path


def get_file():
    path = askopenfilename(title='Select File')
    print(path)
    return path


def file_exists(directory):
    return os.path.isfile(directory)


def folder_exists(directory):
    return os.path.isdir(directory)


def file_path(directory):
    return "." in directory[-8:]


def read_json_file(directory):
    json_file = open(directory)
    json_str = json_file.read()
    json_data = json.loads(json_str)
    json_file.close()
    return json_data


def get_preset(presets_dir, preset_name):
    presets_list = read_json_file(presets_dir)
    preset_dict = [x for x in presets_list if x['name'] == preset_name][0]
    return preset_dict


def write_json_file(directory, content):
    with open(directory, "w") as outfile:
        json.dump(content, outfile)
    outfile.close()


def get_last_used_string(path):
    try:
        file = open(path+LAST_USED_DIR, "r")
        last_used_string = file.readline()
        file.close()
        return last_used_string

    except FileNotFoundError:
        return "No presets have been synced yet."


def update_last_used_string(path):
    f = open(path+LAST_USED_DIR, "w")
    f.write("Last used on "+date.today().strftime("%B %d, %Y"))
    f.close()


def list_unique_located_items(location_one, location_two):
    unique_loc_one, unique_loc_two = [], []
    loc_one_items = get_files_including_subfolders(location_one)
    loc_two_items = get_files_including_subfolders(location_two)
    for item in loc_one_items:
        if item not in loc_two_items:
            unique_loc_one.append(item)
        elif check_file_modified(location_one+"//"+item, location_two+"//"+item):
            unique_loc_one.append(item)
    for item in loc_two_items:
        if item not in loc_one_items:
            unique_loc_two.append(item)
        elif check_file_modified(location_one+"//"+item, location_two+"//"+item):
            unique_loc_two.append(item)
    return unique_loc_one, unique_loc_two


def list_unique_items(location_one, location_two):
    loc_one_items = get_files_including_subfolders(location_one)
    loc_two_items = get_files_including_subfolders(location_two)

    loc_one_set = []
    for item in loc_one_items:
        item_name = item.split("/")[-1]
        item_mod_time = get_modified_time(location_one+"//"+item)
        loc_one_set.append((item, item_name, item_mod_time))

    loc_two_set = []
    for item in loc_two_items:
        item_name = item.split("/")[-1]
        item_mod_time = get_modified_time(location_two+"//"+item)
        loc_two_set.append((item, item_name, item_mod_time))

    for item_dir, item_name, item_mod_time in loc_one_set:
        for item in loc_two_set:
            if item_name == item[1] and item_mod_time == item[2]:
                print(item, "is the same as ", item_dir)
                loc_two_items.remove(item[0])

    for item_dir, item_name, item_mod_time in loc_two_set:
        for item in loc_one_set:
            if item_name == item[1] and item_mod_time == item[2]:
                print(item, "is the same as ", item_dir)
                loc_one_items.remove(item[0])

    return loc_one_items, loc_two_items


def file_selection(event, items, location):
    widget = event.widget
    path = location+"/"+items[widget.curselection()[0]]
    path = path.replace("//", "/")
    path = path.replace("/", "\\")
    open_file_in_explorer(path)


def open_file_in_explorer(directory):
    subprocess.Popen(r'explorer /select,'+directory)
