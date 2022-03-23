import logging
from functools import partial

import hou as hou

from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui

from tools_core.asset_library.asset_browser import AssetBrowserWidget
from tools_core.asset_library import library_manager as lm

from houdini_core.pipeline.lookdev.vray_lookdev import vray_lookdev
from houdini_core.asset_library.megascan_builder import megascan_builder
from houdini_core.pipeline.lighting.vray_lighting import vray_lights


logger = logging.getLogger(__name__)
logger.setLevel(10)


class AssetBrowserUI(QtWidgets.QMainWindow):
    def __init__(self, parent=hou.ui.mainQtWindow()):
        super(AssetBrowserUI, self).__init__(parent)

        self.setWindowTitle("Asset Browser")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.setObjectName("AssetBrowserUI")

        self.dims = (1920, 1080)

        self.setMinimumSize(self.dims[0], self.dims[1])

        self.create_actions()
        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.custom_browser_setup()

    def create_actions(self):
        pass

    def create_custom_actions(self):
        self.custom_actions = {}

        for library in lm.LIBRARIES.keys():
            if not lm.get_library_data(library):
                continue

            self.custom_actions[library] = {}

        # Material Actions
        build_vray_material_action = QtWidgets.QAction("Build VRay Material")

        self.custom_actions["Material"] = [
            {
                "action_object": build_vray_material_action,
                "action_callback": partial(self.build_vray_material_action_callback)
            }
        ]

        # Prop Actions
        build_megascan_action = QtWidgets.QAction("Build Megascan")

        self.custom_actions["Prop"] = [
            {
                "action_object": build_megascan_action,
                "action_callback": partial(self.build_megascan_action_callback),
                "action_asset_data_conditions": ["megascan_id"]
            }
        ]

        # Lights
        import_vray_light_action = QtWidgets.QAction("Create Light")

        self.custom_actions["StudioLights"] = [
            {
                "action_object": import_vray_light_action,
                "action_callback": partial(self.import_vray_light_action_callback)
            }
        ]

        self.custom_actions["HDR"] = [
            {
                "action_object": import_vray_light_action,
                "action_callback": partial(self.import_vray_light_action_callback)
            }
        ]
        self.asset_browser.add_actions_to_menus(self.custom_actions)

    def create_widgets(self):
        self.asset_browser = AssetBrowserWidget.AssetBrowserWidget(dims=self.dims, margin=30)

        self.asset_browser.assets_tw.setColumnWidth(0, self.dims[0] * 0.15)

    def create_layout(self):
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QtWidgets.QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.addWidget(self.asset_browser)

    def create_connections(self):
        pass

    def create_custom_connections(self):
        self.connection_data = []

        self.asset_browser.create_custom_connections(self.connection_data)

    def custom_browser_setup(self):
        # Custom Connections
        self.create_custom_connections()
        self.create_custom_actions()

    def build_vray_material_action_callback(self):
        items = self.asset_browser.assets_tw.selectedItems()

        if not items:
            return

        current_library = items[0].library

        if current_library in lm.STD_LIBRARIES:
            for item in items:
                vray_lookdev.create_vray_material(item.asset_data["materials"][0])

    def import_vray_light_action_callback(self):
        items = self.asset_browser.assets_tw.selectedItems()

        if not items:
            return

        for item in items:
            light_types = {
                "StudioLights": "VRayNodeLightRectangle",
                "HDR": "VRayNodeLightDome"
            }

            vray_lights.create_vray_light(light_types[item.library], path=item.asset_data["asset_path"],
                                          name=item.asset_data["asset_name"])

    def build_megascan_action_callback(self):
        items = self.asset_browser.assets_tw.selectedItems()

        if not items:
            return

        current_library = items[0].library

        if current_library in lm.STD_LIBRARIES:
            for item in items:
                megascan_builder.build_megascan(item.asset_data)


def main():
    dialog = AssetBrowserUI()
    dialog.show()


if __name__ == "__main__":
    main()
