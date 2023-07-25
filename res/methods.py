from PyQt5.QtWidgets import *
from datetime import datetime
import subprocess
import re


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


