import wx
import gui
import os
import sys
import globalPluginHandler
import api
import textInfos
from ui import message
from subprocess import Popen


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    """
    The script will be listed in the input gestures dialog under the "Miscellaneous" category.
    It will have the description "Download Youtube Videos".
    It will be bound to the "NVDA+alt+y"
    """
    scriptCategory = _("Golden Cursor")

    #!#######################################################
    # ? THE SCRIPT STARTS EXCUTING FROM HERE
    #!#######################################################

    def script_start(self, gesture):
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
            ui.message(_("Nothing selected."))

        else:
            ui.message(_("The Script Has Started."))

            link = (info.text)
            SCRIPT_PATH = sys.path[0]
            MAIN_DOWNLOADER_FOLDER = "main_youtube_downloader"
            original_script = os.path.join(SCRIPT_PATH, MAIN_DOWNLOADER_FOLDER,
                                           "original_script.py")
            args = ["python", original_script, link]

            Popen(" ".join(args), shell=True)  # download file

    __gestures = {
        "kb:nvda+control+shift+y": "start",
    }
