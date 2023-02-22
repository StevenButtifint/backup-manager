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


