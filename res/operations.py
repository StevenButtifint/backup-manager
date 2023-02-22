import os
from os import listdir
from os.path import isfile, join


def get_files_only(location):
    files = [f for f in listdir(location) if isfile(join(location, f))]
    return files


