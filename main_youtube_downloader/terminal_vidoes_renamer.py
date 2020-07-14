import os
import webbrowser
import sys
from tkinter import Tk, filedialog
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(SCRIPT_PATH, "settings.txt")

IDM_PATH, DOWNLOAD_FOLDER, CHOOSE_TO_DOWNLOAD_VIDEO, VIDEO_QUALITY = [None]*4

if os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE) as file:
        IDM_PATH, DOWNLOAD_FOLDER, CHOOSE_TO_DOWNLOAD_VIDEO, VIDEO_QUALITY = [
            line.strip() for line in file.readlines()]


def rename_all_in(folder):
    #! DON'T use os.chdir(folder) because this will keep the folder busy
    #! after renaming all the videos and the user will not be able to edit or move this folder
    names = open(os.path.join(folder, "names.txt"))

    sorted_filenames = sorted(os.listdir(folder))
    for file in sorted_filenames:
        # we put the code in try except because the number of files
        # in "sorted_filenames" is bigger than the number of lines in "names.txt" file
        # "sorted_filenames" contains the files we want to rename + other files like  "names.txt" file
        try:
            old = os.path.join(folder, file)
            new = os.path.join(folder, names.readline().strip())
            os.rename(old, new)
        except:
            break


Tk().withdraw()
folder = filedialog.askdirectory()
rename_all_in(folder)
