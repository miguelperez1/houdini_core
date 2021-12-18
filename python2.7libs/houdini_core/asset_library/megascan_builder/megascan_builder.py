import os

import hou as hou

from houdini_core.HouNode import HouNode
from houdini_core.pipeline.lookdev.vray_lookdev import vray_lookdev

material_context = HouNode.HouNode(hou.node("/mat"))
obj_context = HouNode.HouNode(hou.node("/obj"))


def build_megascan(asset_data):
    geo = obj_context.create_node("geo", asset_data["asset_name"])

    file_node = geo.create_node("file", asset_data["asset_name"] + "_file")

    mtl_assignment_node = geo.create_node("material", asset_data["asset_name"] + "_mtl")

    material = vray_lookdev.create_vray_material(asset_data["materials"][0])

    mtl_assignment_node.shop_materialpath1.set(material.node_path())

    file_node.file.set(asset_data["mesh"])

    out_node = geo.create_node("null", asset_data["asset_name"] + "_out")

    out_node.set_input(0, mtl_assignment_node)
    mtl_assignment_node.set_input(0, file_node)

    geo.layout_children()

    out_node.set_display_flag(True)
    out_node.set_render_flag(True)
