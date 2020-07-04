"""
#######################################################
@Author: Karim Elgazar
Contact ME:
Github:
https://github.com/karimelgazar

Linkedin:
https://www.linkedin.com/in/karim-elgazar

Facebook:
https://www.facebook.com/karimCodes

Twitter:
https://www.twitter.com/karimCodes
#######################################################


CHANGES MUST BE DONE AFTER CLONING "pytube" PACKAGE
===========================================================

INSIDE THE "pytube" FOLDER
*****************************
1. In file "extract.py" remove line 1.1 and and put line 1.2
    1.1 ==> parse_qs(formats[i]["cipher"]) for i, data in enumerate(formats)
    1.2 ==> parse_qs(formats[i]["signatureCipher"]) for i, data in enumerate(formats) if "signatureCipher" in formats[i]
    https://github.com/get-pytube/pytube3/pull/80/commits/5ac96de69f025b09abf2a6a24a4103c78b7e4c81#diff-bc809824a75c161c999a237c2fdeedf4

2. Download the file "typing_extensions.py" from the link below and place it inside the "pytube" folder
    https://raw.githubusercontent.com/python/typing/master/typing_extensions/src_py3/test_typing_extensions.py

NOTE
=======
   All the changes above have already been made for this addon so you don't need to
   add any thing I just mentioned them if anything goes wrong ;)
"""


from pytube import YouTube
from pytube.helpers import safe_filename
from youtube_dl import YoutubeDL
import os
import sys
import re
from subprocess import Popen as pop
from pprint import pprint
import argparse

ID_INVALID = -1
ID_VIDEO = 0
ID_PLAYLIST = 1
ID_CHANNEL = 2
BASE_LINK = "www.youtube.com/"
DEFAULT_VIDEO_TITLE = "YouTube.mp4"
DEFAULT_SOUND_TITLE = "Sound.mp3"
UNKNOWN_NAME = "unknown_name"
NANES_FILE = "names.txt"
RES_TO_NUM = {
    "144p": 1,
    "240p": 2,
    "360p": 3,
    "480p": 4
}

NUM_TO_RES = {v: k for (k, v) in RES_TO_NUM.items()}
SETTINGS_FILE = os.path.join(sys.path[0], "settings.txt")
with open(SETTINGS_FILE) as file:
    IDM_DIRECTORY, DOWNLOAD_FOLDER, CHOOSE_TO_DOWNLOAD_VIDEO, VIDEO_QUALITY = [
        line.strip() for line in file.readlines()]

os.chdir(DOWNLOAD_FOLDER)

# make the variable a bool instead of string "True" or String "False"
CHOOSE_TO_DOWNLOAD_VIDEO = (CHOOSE_TO_DOWNLOAD_VIDEO == "True")

# put the path in double quotes because the path may contains spaces
# and we will use this path in terminal
IDM_DIRECTORY = f"\"{IDM_DIRECTORY}\""

#!========================================================================
# JUST FOR TESTING
# --------------------

# p1 = "https://www.youtube.com/playlist?list=PLO1D3YWS7ep3eLiV54GiyRPVJ3XLtjEcx"
# p2 = "https://www.youtube.com/playlist?list=PLO1D3YWS7ep1u30a-rPHnTBMn7duXn9lI"
# p3 = "https://www.youtube.com/playlist?list=PL5tVJtjoxKzp6E5AiMdnL8rFqg5X0iDWX"
# me = "https://www.youtube.com/watch?v=yGrg8IKjrLU"
# pm = "https://www.youtube.com/watch?v=yGrg8IKjrLU&list=PLO1D3YWS7ep0yi84ANyK4yJMDmMon_j5t&index=6&t=75s"
x = "https://www.youtube.com/watch?v=XA6bS8TyN10"
# duck = "https://www.youtube.com/watch?v=nHc288IPFzk&list=PL_90hJucBAcPmFxcbTea81OKGkQevH2F9&index=3"
channel = "https://www.youtube.com/user/thesmallglories/videos"
ar_channel = "https://www.youtube.com/channel/UCxn_DMPZ37eSIXrVxBUc6AA/videos"


#!========================================================================
def type_of(link):

    if (BASE_LINK + "playlist") in link:
        return ID_PLAYLIST

    if (BASE_LINK + "watch") in link:
        return ID_VIDEO

    if "/videos" in link:
        return ID_CHANNEL

    return ID_INVALID


def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def check_and_file_ext(title):
    # return the default title because IDM
    # doesn't accept unicode letters like arabic letters
    if title == UNKNOWN_NAME or (not isEnglish(title)):
        if CHOOSE_TO_DOWNLOAD_VIDEO:
            return DEFAULT_VIDEO_TITLE
        else:
            return DEFAULT_SOUND_TITLE

    # remove characters in range 0-31 (0x00-0x1F)
    # which are not allowed in ntfs (Windows) filenames.
    # Like "#", "?", ">", ...etc
    # see "safe_filename()" method for more INFO.
    if CHOOSE_TO_DOWNLOAD_VIDEO:
        return title + ".mp4"

    return title + ".mp3"


def mkdir_and_chdir(name):
    "make a new folder is not exist and change working directory to it"

    if not os.path.exists(name):
        os.mkdir(name)

    os.chdir(name)


def get_file_name_from(url):
    with YoutubeDL({
        # Download single video instead of a playlist if in doubt.
        "noplaylist": True,
        # to make fetching info faster because we are not interested in DASH info
        "youtube_include_dash_manifest": False,
        # don't print log messages in stdout
            "quiet": True}) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        title = info_dict.get('title', UNKNOWN_NAME)

        # name on youtube without file extension
        title = safe_filename(title)
        # valid name to pass to IDM
        valid_name = check_and_file_ext(title)
        # name on youtube with file extension
        original_name = title + valid_name[-4:] + "\n"

        mkdir_and_chdir(title)
        with open(NANES_FILE, 'w') as file:
            file.write(original_name)

        return valid_name


def download_with_IDM(direct_link=None, file_name=None,
                      download_path=DOWNLOAD_FOLDER, start=False):
    """
    download the links with idm after extracting
    you should see this link to see all the avilable
    parameter that you can pass in the terminal
    https://www.internetdownloadmanager.com/support/command_line.html


    Arguments:
        directory  -- the output directory where the links txt file
        links_txt  -- the txt file that has the direct links
        start      -- start the queue in IDM
    """
    global IDM_DIRECTORY

    no_questions = ' /n'
    add_to_queue = ' /a'
    start_queue = ' /s'
    try:
        download_link = ' /d \"{}\"'.format(direct_link.strip())
        local_path = ' /p \"{}\"'.format(download_path.replace('/', '\\'))
        local_file_name = ' /f \"{}\"'.format(file_name.strip())
        # file_name = re.sub(
        #     r"[*:/<>?\|]", "_", file_name)

        #! the program will name arabic files as WHY...????
        #! Beacause windows doesn't support passing utf-8
        #! parameters in the terminal so IDM will get the name wrong as ????

        # ? change terminal code page to UTF-8 BUT DID NOT WORK EITHER
        # change_terminal_to_utf_8 = "chcp 65001"
        # pop(change_terminal_to_utf_8, shell=True)

        COMMAND = IDM_DIRECTORY + download_link + \
            local_path + local_file_name + no_questions + add_to_queue

        print(COMMAND, start, sep='\n')
        print('='*50)
        # pop(COMMAND, shell=True)  # download file
    except:
        pass

    # we need to check if this file is the last one so we can start the queue
    # because you can't add a file (the last file) if the queue was running
    if start:
        # print('STARTED')
        pop(IDM_DIRECTORY + start_queue, shell=True)


def get_direct_link(url):
    video = YouTube(url)
    stream = None
    if not CHOOSE_TO_DOWNLOAD_VIDEO:
        stream = video.streams.get_audio_only()

    elif VIDEO_QUALITY == 'max':
        """
        WHY the "get_highest_resolution()" method returns only "720p" resolution?
        ==============================================================================
        You may notice that some streams listed have both a video codec and audio codec,
        while others have just video or just audio, this is a result of YouTube supporting
        a streaming technique called Dynamic Adaptive Streaming over HTTP (DASH).

        In the context of pytube, the implications are for the highest quality streams;
        you now need to download both the audio and video tracks and then post-process
        them with software like FFmpeg to merge them.

        The legacy streams that contain the audio and video in a single file
        (referred to as "progressive download") are still available, but only for resolutions 720p and below.
        """
        stream = video.streams.get_highest_resolution()

    else:
        # the given "VIDEO_QUALITY" might not be avilable to download
        # so the method "get_by_resolution" will return None so we decrease the
        # video resolution to the nearest quality
        i = RES_TO_NUM.get(VIDEO_QUALITY)
        while i > 0 and stream == None:
            stream = video.streams.get_by_resolution(NUM_TO_RES.get(i))
            i += -1

    if stream == None:
        stream = video.streams.get_lowest_resolution()

    return stream.url


def download_multiple_videos(pl_ch_object, name):
    with open(NANES_FILE, "w") as file:
        for i, video in enumerate(pl_ch_object.get('entries')):
            link_video, title = None, UNKNOWN_NAME
            try:
                link_video = "https://www.youtube.com/watch?v=" + \
                    video.get('id')
                title = video.get('title', UNKNOWN_NAME)
                # print(title)

            except:
                continue

            title = safe_filename(title)
            download_link = get_direct_link(link_video)
            valid_name = str(i + 1).zfill(2) + "-" + check_and_file_ext(title)
            original_name = str(i + 1).zfill(2) + "-" + \
                title + valid_name[-4:] + "\n"

            file.write(original_name)
            download_with_IDM(direct_link=download_link,
                              file_name=valid_name,
                              download_path=os.path.join(DOWNLOAD_FOLDER,
                                                         name))

    # start the queue in IDM
    download_with_IDM(start=True)


def download_playlist(url):
    ydl = YoutubeDL({
        # this line is VERY IMPORTANT because if there's private viedeos
        # or anything unavilable to download youtube-dl won't crash
        # and will continue to the next videos in the playlist
        "ignoreerrors": True,
        # to make fetching info faster because we are not interested in DASH info
        "youtube_include_dash_manifest": False,
        # don't print log messages in stdout
        "quiet": True})

    with ydl:
        playlist = ydl.extract_info(
            url,
            download=False  # We just want to extract the info
        )

    name_playlist = safe_filename(playlist.get('title'))
    mkdir_and_chdir(name_playlist)
    download_multiple_videos(playlist, name_playlist)


def download_channel(url):
    ydl = YoutubeDL({
        # this line is VERY IMPORTANT because if there's private viedeos
        # or anything unavilable to download youtube-dl won't crash
        # and will continue to the next videos in the playlist
        "ignoreerrors": True,
        # Download single video instead of a playlist if in doubt.
        "noplaylist": True,
        # to make fetching info faster because we are not interested in DASH info
        "youtube_include_dash_manifest": False,
        # don't print log messages in stdout
        "quiet": True})

    with ydl:
        channel = ydl.extract_info(
            url,
            download=False  # We just want to extract the info
        )

    print("="*50)

    # original output without split is "Uploads from CHANNEL_NAME" (quotes not included)
    # so we need to split and pick the last item
    name_channel = safe_filename(channel.get("title").split(' from ')[-1])
    print(name_channel)
    print("="*50)
    mkdir_and_chdir(name_channel)
    download_multiple_videos(channel, name_channel)


def get_link_from_terminal():
    """
    get the link passed in the terminal
    """

    # ? تجهيز الترمينال
    parser = argparse.ArgumentParser()
    arg_help = '''
            The Link To The Video, Playlist, Or Channel'''

    parser.add_argument('link',
                        help=arg_help)

    passed_link = parser.parse_args().link

    return passed_link.strip()


def check_link_and_download():
    url = get_link_from_terminal()
    link_id = type_of(url)

    if link_id == ID_INVALID:
        sys.exit()

    elif link_id == ID_VIDEO:
        download_link = get_direct_link(url)
        name = get_file_name_from(url)
        download_with_IDM(direct_link=download_link,
                          file_name=name,
                          start=True)
        return

    elif link_id == ID_PLAYLIST:
        download_playlist(url)
        return

    else:
        download_channel(url)

#!#######################################################
# ? THE SCRIPT STARTS EXCUTING FROM HERE
#!#######################################################


check_link_and_download()
#     # x)
# channel)
# "https://www.youtube.com/playlist?list=PLiWvewi88jEIH9fCjxdqFdLESqt9L2lu3")
# "https://www.youtube.com/watch?v=xCF6pjIWYAQ&list=PLiWvewi88jEIH9fCjxdqFdLESqt9L2lu3&index=3&t=0s")
