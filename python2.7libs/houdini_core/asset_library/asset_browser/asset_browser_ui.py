import logging
from functools import partial

import hou as hou

from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui

from tools_core.asset_library.asset_browser import AssetBrowserWidget
from tools_core.asset_library import library_manager as lm

logger = logging.getLogger(__name__)
logger.setLevel(10)


class ExampleDialog(QtWidgets.QMainWindow):
    def __init__(self, parent=hou.ui.mainQtWindow()):
        super(ExampleDialog, self).__init__(parent)

        self.setWindowTitle("Window")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.setObjectName("ExampleDialog")

        self.dims = (1920, 1080)

        self.setMinimumSize(self.dims[0], self.dims[1])

        self.create_actions()
        self.create_widgets()
        self.create_layout()
        self.create_connections()
        # self.custom_browser_setup()

    def create_actions(self):
        pass

    def create_custom_actions(self):
        self.custom_actions = {}

        for library in lm.LIBRARIES.keys():
            if not lm.get_library_data(library):
                continue

            self.custom_actions[library] = {}

        self.asset_browser.add_actions_to_menus(self.custom_actions)

    def create_widgets(self):
        self.asset_browser = AssetBrowserWidget.AssetBrowserWidget(dims=self.dims)

    def create_layout(self):
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QtWidgets.QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.addWidget(self.asset_browser)

    def create_connections(self):
        pass

    def create_custom_connections(self):
        self.connection_data = [
            {
                "widget": "assets_tw",
                "signal": "itemClicked",
                "function": ""
            }
        ]

        self.asset_browser.create_custom_connections(self.connection_data)

    def custom_browser_setup(self):
        # Custom Connections
        self.create_custom_connections()
        self.create_custom_actions()


def main():
    dialog = ExampleDialog()
    dialog.show()


if __name__ == "__main__":
    main()
