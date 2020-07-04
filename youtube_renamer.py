import wx
import gui
import os
from ui import message
import globalPluginHandler


class YoutubeRenamer(wx.Dialog):

    def __init__(self, parent):
        super(YoutubeRenamer, self).__init__(
            parent, title=_("downloder"), size=(320, 300))
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        sHelper = gui.guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)
        bHelper = gui.guiHelper.ButtonHelper(orientation=wx.HORIZONTAL)

        # ? Videos FOLDER
        DirectoryButtonID = wx.NewIdRef() if wx.version().startswith("4") else wx.NewId()
        bHelper.addButton(self, DirectoryButtonID, _(
            "&VideosFolder"), wx.DefaultPosition)
        self.Bind(wx.EVT_BUTTON, self.on_choose_dir, id=DirectoryButtonID)

    def rename_all_in(self, folder):
        os.chdir(folder)
        names = open("names.txt")

        sorted_filenames = sorted(os.listdir(folder))
        for file in sorted_filenames:
            # we put the code in try except because the number of files
            # in "sorted_filenames" is bigger than the number of lines in "names.txt" file
            # "sorted_filenames" contains the files we want to rename + other files like  "names.txt" file
            try:
                os.rename(file, names.readline().strip())
            except:
                break

    def on_choose_dir(self, event):
        chosen = False
        folder = ""
        while not chosen:
            # otherwise ask the user what new file to open
            with wx.DirDialog(self, "Select Videos Folder", defaultPath="",
                              style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as folderDialog:

                if folderDialog.ShowModal() == wx.ID_OK:
                    chosen = True   # the user changed their mind

                # Proceed loading the file chosen by the user
                folder = folderDialog.GetPath()

        self.rename_all_in(folder)
        message(_("All Videos Has Been Renamed"))


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    scriptCategory = _("Golden Cursor")

    def script_youtube_rename(self, gesture):
        d = YoutubeRenamer(parent=gui.mainFrame)
        gui.mainFrame.prePopup()
        d.Raise()
        d.Show()
        gui.mainFrame.postPopup()

    __gestures = {
        "kb:nvda+control+shift+r": "youtube_rename",
    }
