# -*- coding: utf-8 -*-
import wx
import gui
import os
import sys
import globalPluginHandler
from .import youtube_settinsgs
from .import youtube_renamer
import api
import textInfos
from ui import message
from subprocess import Popen, PIPE
import addonHandler
addonHandler.initTranslation()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

    scriptCategory = _("youtubeDownloader")

    #!#######################################################
    # ? THE SCRIPT STARTS EXCUTING FROM HERE
    #!#######################################################

    def script_start(self, gesture):
        """
        get the current selected text and pass it to "orignal_script.py" file
        Its shortcut is "alt+control+y"
        """
        obj = api.getFocusObject()
        treeInterceptor = obj.treeInterceptor
        if hasattr(treeInterceptor, 'TextInfo') and not treeInterceptor.passThrough:
            obj = treeInterceptor

        try:
            info = obj.makeTextInfo(textInfos.POSITION_SELECTION)
        except (RuntimeError, NotImplementedError):
            info = None

        if not info or info.isCollapsed:
            # Translators: This message is spoken if there's no selection.
            message(_("Nothing selected."))

        else:
            message(_("The Script Has Started."))

            link = (info.text)
            SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
            MAIN_DOWNLOADER_FOLDER = "main_youtube_downloader"
            original_script = os.path.join(SCRIPT_PATH, MAIN_DOWNLOADER_FOLDER,
                                           "original_script.py")

            #! use the orignal python because NVDA doesn't understand "orignal_script.py" imports
            python_path = os.path.join(SCRIPT_PATH, "python", "python.exe")
            args = [python_path, original_script, link]
            Popen(" ".join(args), shell=True)  # download file

    script_start.__doc__ = _('start download')

    def script_youtube_downloader_settings(self, gesture):
        """
        open settings menu 
        """
        d = youtube_settinsgs.YoutubeDownloderSettings(parent=gui.mainFrame)
        gui.mainFrame.prePopup()
        d.Raise()
        d.Show()
        gui.mainFrame.postPopup()
    script_youtube_downloader_settings.__doc__ = _(
        'open youtubedownloader settings')

    def script_youtube_rename(self, gesture):
        """
        open gui to select folder contaning the videos to rename
        """
        d = youtube_renamer.YoutubeRenamer(parent=gui.mainFrame)
        gui.mainFrame.prePopup()
        d.Raise()
        d.Show()
        gui.mainFrame.postPopup()
        self.terminate()
    script_youtube_rename.__doc__ = _('youtube rename files')

    __gestures = {
        "kb:alt+control+y": "start",
        "kb:alt+control+r": "youtube_rename",
        "kb:alt+control+l": "youtube_downloader_settings",
    }
