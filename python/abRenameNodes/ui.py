"""
    Qt widget for the `abRenameNodes` tool
"""
import os
import hou
from hutil.Qt import QtCore, QtWidgets, QtUiTools

from . import core as renamer_core


RESOURCES = os.path.join(os.path.dirname(__file__), "resources")
NODE_RENAMER = None


class HoudiniNodeRenamer(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.__start = 1

        self.ui = self.load_widget()
        self.setCentralWidget(self.ui)
        self.connect_widgets()
        self.update_preview()

    def load_widget(self):
        loader = QtUiTools.QUiLoader()
        file = QtCore.QFile(os.path.join(RESOURCES, "renamer_widget.ui"))
        file.open(QtCore.QFile.ReadOnly)
        widget = loader.load(file)
        file.close()
        return widget

    def connect_widgets(self):
        self.ui.button_name.clicked.connect(self.do_rename)
        self.ui.button_prefix.clicked.connect(self.do_prefix)
        self.ui.button_suffix.clicked.connect(self.do_suffix)
        self.ui.line_name.textChanged.connect(self.update_preview)
        self.ui.line_prefix.textChanged.connect(self.update_preview)
        self.ui.line_suffix.textChanged.connect(self.update_preview)

    def do_rename(self):
        name = self.ui.line_name.text()
        prefix = self.ui.line_prefix.text()
        suffix = self.ui.line_suffix.text()
        renamer_core.rename_selection(name, prefix, suffix)
        self.update_preview()

    def do_prefix(self):
        prefix = self.ui.line_prefix.text()
        renamer_core.prefix_selection(prefix)
        self.update_preview()

    def do_suffix(self):
        suffix = self.ui.line_suffix.text()
        renamer_core.suffix_selection(suffix)
        self.update_preview()

    def update_preview(self):
        self.__start = 1
        self.ui.list_preview.clear()

        name = self.ui.line_name.text()
        prefix = self.ui.line_prefix.text()
        suffix = self.ui.line_suffix.text()

        for item in renamer_core.get_selected():
            preview_name = prefix + name + f'_{self.__start:0>3}' + suffix
            item_name = f"{item.name()} -> {preview_name}"
            self.ui.list_preview.addItem(item_name)
            self.__start += 1


def open_ui() -> HoudiniNodeRenamer:
    """ Open the Dart Data Prep window. """
    global NODE_RENAMER

    if not NODE_RENAMER:
        NODE_RENAMER = HoudiniNodeRenamer()

    NODE_RENAMER.setParent(hou.qt.mainWindow(), QtCore.Qt.Window)
    NODE_RENAMER.setFocus(QtCore.Qt.FocusReason())
    NODE_RENAMER.activateWindow()
    NODE_RENAMER.show()

    return NODE_RENAMER
