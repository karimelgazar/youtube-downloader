# -*- coding: utf-8 -*-
import addonHandler
addonHandler.initTranslation() 
import wx
import gui
import os
from ui import message
import webbrowser

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
# SCRIPT_PATH = sys.path[0]
MAIN_DOWNLOADER_FOLDER = "main_youtube_downloader"
SETTINGS_FILE = os.path.join(
    SCRIPT_PATH, MAIN_DOWNLOADER_FOLDER, "settings.txt")

IDM_PATH, DOWNLOAD_FOLDER, CHOOSE_TO_DOWNLOAD_VIDEO, VIDEO_QUALITY = [None]*4

if os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE) as file:
        IDM_PATH, DOWNLOAD_FOLDER, CHOOSE_TO_DOWNLOAD_VIDEO, VIDEO_QUALITY = [
            line.strip() for line in file.readlines()]


class YoutubeRenamer(wx.Dialog):

    def __init__(self, parent):
        super(YoutubeRenamer, self).__init__(
            parent, title=_("rename videos"), size=(320, 300))
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        sHelper = gui.guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)
        bHelper = gui.guiHelper.ButtonHelper(orientation=wx.HORIZONTAL)

        # ? Videos FOLDER
        DirectoryButtonID = wx.NewIdRef() if wx.version().startswith("4") else wx.NewId()
        bHelper.addButton(self, DirectoryButtonID, _(
            _("&VideosFolder")), wx.DefaultPosition)
        self.Bind(wx.EVT_BUTTON, self.on_choose_dir, id=DirectoryButtonID)

        # ? X close button
        self.Bind(wx.EVT_CLOSE, self.onClose)

        self.EscapeId = wx.ID_CLOSE
        mainSizer.Add(
            sHelper.sizer, border=gui.guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
        self.Sizer = mainSizer
        mainSizer.Fit(self)

    def rename_all_in(self, folder):
        #! DON'T use os.chdir(folder) because this will keep the folder busy
        #! after renaming all the videos and the user will not be able to edit or move this folder
        names = open(os.path.join(folder, "names.txt"))

        sorted_filenames = sorted(os.listdir(folder))
        for file in sorted_filenames:
            # we put the code in try except because the number of files
            # "sorted_filenames" contains the files we want to rename + other files like
            # "names.txt" file in "sorted_filenames" is bigger than the number
            # of lines in "names.txt" file
            try:
                old = os.path.join(folder, file)
                new = os.path.join(folder, names.readline().strip())
                os.rename(old, new)
            except:
                break


    def on_choose_dir(self, event):
        global DOWNLOAD_FOLDER
        message(_("Choose The Folder Of The Videos You Want To Rename"))
        folder = ""

        with wx.DirDialog(self, _("Select Videos Folder"), defaultPath=DOWNLOAD_FOLDER,
                          style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as folderDialog:

            if DOWNLOAD_FOLDER != None:
                folderDialog.SetPath(DOWNLOAD_FOLDER)

            if folderDialog.ShowModal() == wx.ID_CANCEL:
                message(_("No Folder Selected Exiting The Program"))
                self.Destroy()
                return

            # Proceed loading the file chosen by the user
            folder = folderDialog.GetPath()

            message(_("The Folder Has Been Chosen"))
            self.rename_all_in(folder)

        message(_("All Videos Have Been Renamed"))
        webbrowser.open(folder)  # ? open videos folder
        self.Destroy()

    def onClose(self, evt):
        self.Destroy()    