import wx
import gui
import os
import sys
from ui import message
import globalPluginHandler


IDM_PATH, DOWNLOAD_FOLDER, CHOOSE_TO_DOWNLOAD_VIDEO, VIDEO_QUALITY = [
    None]*4

LEVEL = ('144p', '240p', '360p', '480p', '720p')


class YoutubeDownloderSettings(wx.Dialog):

    def __init__(self, parent):
        global IDM_PATH, DOWNLOAD_FOLDER, CHOOSE_TO_DOWNLOAD_VIDEO, VIDEO_QUALITY

        # TODO make option for dowbload audio only nothing else
        # TODO make option to select installed python path
        # TODO make option to select script path

        super(YoutubeDownloderSettings, self).__init__(
            parent, title=_("downloder"), size=(320, 300))
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        sHelper = gui.guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)
        bHelper = gui.guiHelper.ButtonHelper(orientation=wx.HORIZONTAL)

        # ? IDM
        PIDmanButtonID = wx.NewIdRef() if wx.version().startswith("4") else wx.NewId()
        bHelper.addButton(self, PIDmanButtonID, _(
            "&PathIDman"), wx.DefaultPosition)
        self.Bind(wx.EVT_BUTTON, self.on_choose_IDM, id=PIDmanButtonID)

        # ? DOWNLOAD FOLDER
        DirectoryButtonID = wx.NewIdRef() if wx.version().startswith("4") else wx.NewId()
        bHelper.addButton(self, DirectoryButtonID, _(
            "&DownloadFolder"), wx.DefaultPosition)
        self.Bind(wx.EVT_BUTTON, self.on_choose_dir, id=DirectoryButtonID)

        # # ? Script Path
        # DirectoryButtonID = wx.NewIdRef() if wx.version().startswith("4") else wx.NewId()
        # bHelper.addButton(self, DirectoryButtonID, _(
        #     "&ScriptPath"), wx.DefaultPosition)
        # self.Bind(wx.EVT_BUTTON, self.on_choose_script, id=DirectoryButtonID)

        # ? Quality ComboBox
        self.WCombo = sHelper.addLabeledControl(
            _("&ChooseQuality"), wx.Choice, choices=(LEVEL))
        self.WCombo.SetFocus()
        self.WCombo.SetSelection(4)

        #self.FCombo = sHelper.addLabeledControl(_("&ChooseQuality"), wx.Choice, choices = (LEVEL))
        self.ACheckBox = sHelper.addItem(
            wx.CheckBox(self, label=_("&Download Audio Only")))
        # # self.ACheckBox.SetValue(config.conf["quickAccess"]["unprotectControls"])
        # self.VCheckBox = sHelper.addItem(
        #     wx.CheckBox(self, label=_("&DownloadVidio")))
        # self.VCheckBox.SetValue(config.conf["quickAccess"]["unprotectControls"])

        bHelper.addButton(self, wx.ID_CLOSE, _("&Close"), wx.DefaultPosition)
        sHelper.addItem(bHelper)
        self.Bind(wx.EVT_BUTTON, self.onClose, id=wx.ID_CLOSE)

        # self.Bind(wx.EVT_BUTTON, lambda evt: self.Close(), id=wx.ID_CLOSE)
        # self.Bind(wx.EVT_CLOSE, self.onClose)

        self.EscapeId = wx.ID_CLOSE
        mainSizer.Add(
            sHelper.sizer, border=gui.guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
        self.Sizer = mainSizer
        mainSizer.Fit(self)

    def on_choose_IDM(self, event):

        chosen = False

        while not chosen:
            # otherwise ask the user what new file to open
            with wx.FileDialog(self, "Select idman.exe file", wildcard="*.exe",
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

                if fileDialog.ShowModal() == wx.ID_OK:
                    chosen = True   # the user changed their mind

                # Proceed loading the file chosen by the user
                IDM_PATH = fileDialog.GetPath()

                if "idman" not in IDM_PATH.lower():
                    continue

    def on_choose_dir(self, event):
        chosen = False

        while not chosen:
            # otherwise ask the user what new file to open
            with wx.DirDialog(self, "Select Download Folder", defaultPath="",
                              style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as folderDialog:

                if folderDialog.ShowModal() == wx.ID_OK:
                    chosen = True   # the user changed their mind

                # Proceed loading the file chosen by the user
                DOWNLOAD_FOLDER = folderDialog.GetPath()

        # message(_('rename'))

    # def on_choose_script(self, event):
    #     message(_('rename'))

    def onClose(self, evt):
        global IDM_PATH, DOWNLOAD_FOLDER, CHOOSE_TO_DOWNLOAD_VIDEO, VIDEO_QUALITY

        SCRIPT_PATH = sys.path[0]
        MAIN_DOWNLOADER_FOLDER = "main_youtube_downloader"

        CHOOSE_TO_DOWNLOAD_VIDEO = (not self.ACheckBox.IsChecked())
        chosen_index = self.WCombo.GetSelection()
        if chosen_index == 4:
            VIDEO_QUALITY = "max"
        else:
            VIDEO_QUALITY = LEVEL[chosen_index]

        with open(os.path.join(SCRIPT_PATH, MAIN_DOWNLOADER_FOLDER,
                               "settings.txt"), 'w') as txt:
            print(
                IDM_PATH,
                DOWNLOAD_FOLDER,
                CHOOSE_TO_DOWNLOAD_VIDEO,
                VIDEO_QUALITY,
                sep="\n",
                file=txt)


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    scriptCategory = _("Golden Cursor")

    def script_youtube_downloader_settings(self, gesture):
        d = YoutubeDownloderSettings(parent=gui.mainFrame)
        gui.mainFrame.prePopup()
        d.Raise()
        d.Show()
        gui.mainFrame.postPopup()

    __gestures = {
        "kb:nvda+control+shift+l": "youtube_downloader_settings",
    }
