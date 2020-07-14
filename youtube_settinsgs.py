# -*- coding: utf-8 -*-

import wx
import gui
import os
import sys
from ui import message
import webbrowser
import addonHandler
addonHandler.initTranslation()

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
MAIN_DOWNLOADER_FOLDER = "main_youtube_downloader"
SETTINGS_FILE = os.path.join(
    SCRIPT_PATH, MAIN_DOWNLOADER_FOLDER, "settings.txt")

IDM_PATH, DOWNLOAD_FOLDER, CHOOSE_TO_DOWNLOAD_VIDEO, VIDEO_QUALITY = [None]*4

if os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE) as file:
        IDM_PATH, DOWNLOAD_FOLDER, CHOOSE_TO_DOWNLOAD_VIDEO, VIDEO_QUALITY = [
            line.strip() for line in file.readlines()]

# ? VIDEO QUALITY
LEVEL = ('144p', '240p', '360p', '480p', '720p')


class YoutubeDownloderSettings(wx.Dialog):

    def __init__(self, parent):
        global IDM_PATH, DOWNLOAD_FOLDER, CHOOSE_TO_DOWNLOAD_VIDEO, VIDEO_QUALITY, LEVEL

        super(YoutubeDownloderSettings, self).__init__(
            parent, title=_("downloder"), size=(320, 300))
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        sHelper = gui.guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)
        bHelper = gui.guiHelper.ButtonHelper(orientation=wx.HORIZONTAL)

        # ? IDM
        was_found, pathIDM = self.chech_if_IDM_EXIST()

        if was_found:
            IDM_PATH = pathIDM

        else:
            PIDmanButtonID = wx.NewIdRef() if wx.version().startswith("4") else wx.NewId()
            bHelper.addButton(self, PIDmanButtonID, _(
                "&PathIDman"), wx.DefaultPosition)
            self.Bind(wx.EVT_BUTTON, self.on_choose_IDM, id=PIDmanButtonID)

        # ? DOWNLOAD FOLDER
        DirectoryButtonID = wx.NewIdRef() if wx.version().startswith("4") else wx.NewId()
        bHelper.addButton(self, DirectoryButtonID, _(
            _("&DownloadFolder")), wx.DefaultPosition)
        self.Bind(wx.EVT_BUTTON, self.on_choose_dir, id=DirectoryButtonID)

        # ? Quality ComboBox
        self.WCombo = sHelper.addLabeledControl(
            _("&ChooseQuality"), wx.Choice, choices=(LEVEL))
        self.WCombo.SetFocus()

        if VIDEO_QUALITY != None:
            if VIDEO_QUALITY == "max":
                self.WCombo.SetSelection(4)
            else:
                self.WCombo.SetSelection(LEVEL.index(VIDEO_QUALITY))
        else:
            self.WCombo.SetSelection(3)

        # ? Chechbox Download Audio Only
        self.ACheckBox = sHelper.addItem(
            wx.CheckBox(self, label=_("&Download Audio Only")))
        if CHOOSE_TO_DOWNLOAD_VIDEO != None:
            self.ACheckBox.SetValue(CHOOSE_TO_DOWNLOAD_VIDEO != True)
        else:
            self.ACheckBox.SetValue(False)

        # ? Close Button
        bHelper.addButton(self, wx.ID_CLOSE, _("&Close"), wx.DefaultPosition)
        sHelper.addItem(bHelper)
        self.Bind(wx.EVT_BUTTON, self.onClose, id=wx.ID_CLOSE)

        # ? X close button
        self.Bind(wx.EVT_CLOSE, self.onClose)

        self.EscapeId = wx.ID_CLOSE
        mainSizer.Add(
            sHelper.sizer, border=gui.guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
        self.Sizer = mainSizer
        mainSizer.Fit(self)

    def chech_if_IDM_EXIST(self):
        PATH = "C:\\Program Files\\Internet Download Manager\\IDMan.exe"
        if os.path.exists(PATH):
            message(_("Internet Download Manager Was Found."))
            return True, PATH

        PATH = "C:\\Program Files (x86)\\Internet Download Manager\\IDMan.exe"
        if os.path.exists(PATH):
            message(_("Internet Download Manager Was Found."))
            return True, PATH

        else:
            msg = (
                _('Internet Download Manager Was Not Found in the C Partition, do you want to Downloads it?'))
            message(msg)

            d = wx.MessageDialog(None, (msg), wx.MessageBoxCaptionStr, wx.YES |
                                 wx.NO | wx.ICON_WARNING)
            if d.ShowModal() == wx.ID_YES:
                ui.message("Opening Internet Download Manager Website")
                s = "http://www.internetdownloadmanager.com/download.html"
                webbrowser.open(s)
                self.Destroy()
            else:
                message(_('OK Please Select It'))

            return False, None

    def on_choose_IDM(self, event):
        global IDM_PATH
        chosen = False

        with wx.FileDialog(self, "Select idman.exe file", wildcard="idman.exe",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if IDM_PATH != None:
                fileDialog.SetPath(IDM_PATH)
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                self.Destroy()

            # Proceed loading the file chosen by the user
            IDM_PATH = fileDialog.GetPath()

            if "idman" not in IDM_PATH.lower():
                self.Destroy()

    def on_choose_dir(self, event):
        global DOWNLOAD_FOLDER
        chosen = False

        with wx.DirDialog(self, _("Select Download Folder"), defaultPath="",
                          style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as folderDialog:

            if DOWNLOAD_FOLDER != None:
                folderDialog.SetPath(DOWNLOAD_FOLDER)

            if folderDialog.ShowModal() == wx.ID_CANCEL:
                message(_("No Folder Selected Exiting The Program"))
                self.Destroy()
                return

            # Proceed loading the file chosen by the user
            DOWNLOAD_FOLDER = folderDialog.GetPath()

    def onClose(self, evt):
        global IDM_PATH, DOWNLOAD_FOLDER, CHOOSE_TO_DOWNLOAD_VIDEO, VIDEO_QUALITY, SETTINGS_FILE, LEVEL

        CHOOSE_TO_DOWNLOAD_VIDEO = (not self.ACheckBox.IsChecked())
        chosen_index = self.WCombo.GetSelection()
        if chosen_index == 4:
            VIDEO_QUALITY = "max"
        else:
            VIDEO_QUALITY = LEVEL[chosen_index]

        with open(SETTINGS_FILE, 'w') as txt:
            print(
                IDM_PATH,
                DOWNLOAD_FOLDER,
                CHOOSE_TO_DOWNLOAD_VIDEO,
                VIDEO_QUALITY,
                sep="\n",
                file=txt)

        self.Destroy()
