from tkinter import filedialog, Tk
import os
import sys

SCRIPT_PATH = sys.path[0]
print(SCRIPT_PATH)


LINE_SEP = '=' * 50


def pick_download_folder():
    """
    This method launch a folder picker to choose
    the root download folder 
    """
    where_to = ''
    while not where_to:
        # Pick download folder
        print('\nplease choose where is your download folder.'.title())
        print(LINE_SEP)
        Tk().withdraw()  # to hide the small tk window
        where_to = filedialog.askdirectory()  # folder picker

    print("DONE")
    return os.path.abspath(where_to)


def pick_idm_exe():
    """
    This method launch a file picker to choosethe idman.exe file
    """
    where_to = ''
    while not where_to:
        # Pick download folder
        print('\nplease choose the correct {} file.'.title().format("\"idman.exe\""))
        print(LINE_SEP)
        Tk().withdraw()  # to hide the small tk window
        where_to = filedialog.askopenfilename()  # file picker

        if not where_to.lower().endswith('idman.exe'):
            where_to = ''

    print("DONE")
    return os.path.abspath(where_to)


def start_queue_or_not():
    """
    this method let the user enter any value to choose whether to start queue
    after adding all direct links or not.
    if the entered value is:
        1. number zero: the idm will not start queue
        2. any other value will start queue
    """

    choose_to_start_queue = ''
    while not choose_to_start_queue:
        start = input("""please, choose whether to start queue after adding all direct links or not:
                  if the entered value is :
                  1. number zero: the idm will not start queue
                  2. any other value will start queue
                  the value: """)

        choose_to_start_queue = choose_to_start_queue.strip()

    print(LINE_SEP)

    if choose_to_start_queue == '0':
        print("DONE")
        return False

    print("DONE")
    return True


def choose_download_video_or_not():
    """
    this method let the user enter a value to choose whether to download video or audio
            the value to enter is:
                  number zero: for audio
                  any other value for video
    """
    print('\nplease choose whether to download video or audio.'.title())
    print(LINE_SEP)
    choose_to_start_queue = ''
    while not choose_to_start_queue:
        print("enter number zero: for audio".title())
        print("enter any other value for video".title())
        choose_to_start_queue = input("please, enter the value: ".title())

        choose_to_start_queue = choose_to_start_queue.strip()

    if choose_to_start_queue == '0':
        print("DONE")
        return False

    print("DONE")
    return True


def choose_video_quality():
    """
    choose video quality to download from number 1 to 4
    if anything else was enterd the video maximum quality will be chosen
    """
    print('\nPlease, Enter the Number of your prefered Qaulity.')
    print(LINE_SEP)
    print('144p   ==  Enter Number 1')
    print('240p   ==  Enter Number 2')
    print('360p   ==  Enter Number 3')
    print('480p   ==  Enter Number 4')
    # print('720p   ==  Enter Number 5')

    quality_dict = {"1": '144p', "2": '240p', "3": '360p', "4": "480p"}

    print('\nPlease, Choose a number between 1 to 4: ')
    num = input('Enter Quality Number: ')

    quality = quality_dict.get(num)
    if quality == None:
        print("\nOK I\'ll download it at maximum quality.".title())
    else:
        print('\nOK I\'ll download it at: %s.' % quality)

    print("DONE")
    print(LINE_SEP)

    return quality


#!#######################################################
# ? THE SCRIPT STARTS EXCUTING FROM HERE
#!#######################################################

with open(os.path.join(SCRIPT_PATH, "settings.txt"), 'w') as txt:
    print(
        pick_idm_exe(),
        pick_download_folder(),
        sep="\n",
        file=txt)

    video_or_audio = choose_download_video_or_not()
    txt.write(str(video_or_audio) + "\n")

    quality = "max"
    if video_or_audio:
        quality = choose_video_quality()

    txt.write(quality + "\n")
