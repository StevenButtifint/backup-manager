import win32api
import shutil
import os
import json
import subprocess
import tkinter as tk
from tkinter.filedialog import askdirectory, askopenfilename
from os import listdir
from datetime import date
from os.path import isfile, join


from res.constants import *


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


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


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
    path = askdirectory(title='Select Folder')  # shows dialog box and return the path
    print(path)
    return path


def get_file():
    path = askopenfilename(title='Select File')
    print(path)
    return path


def add_file(entry):
    path = get_file()
    entry.config(state="normal")
    entry.delete(0, tk.END)
    entry.insert(0, path)
    entry.config(state="readonly")


def add_folder(entry):
    path = get_folder()
    entry.config(state="normal")
    entry.delete(0, tk.END)
    entry.insert(0, path)
    entry.config(state="readonly")


def file_exists(directory):
    return os.path.isfile(directory)


def folder_exists(directory):
    return os.path.isdir(directory)


def file_path(directory):
    return "." in directory[-8:]


def get_saved_presets():
    try:
        json_file = open(resource_path(PRESETS_DIR))
        json_str = json_file.read()
        json_data = json.loads(json_str)
    except FileNotFoundError:
        with open(resource_path(PRESETS_DIR), "w") as outfile:
            json.dump("[]", outfile)
        json_data = json.loads("[]")
    return json_data


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




def file_selection(event, items, location):
    widget = event.widget
    path = location+"/"+items[widget.curselection()[0]]
    path = path.replace("//", "/")
    path = path.replace("/", "\\")
    open_file_in_explorer(path)


def open_file_in_explorer(directory):
    subprocess.Popen(r'explorer /select,'+directory)
