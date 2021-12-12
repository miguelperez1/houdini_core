import os

import hou as hou

from HouNode import HouNode


VRAYMTL_CONNECTIONS = {
    'diffuse': 0,
    'gloss': 8,
    'normal': 5,
    'specular': 7
}

MTL_CONNECTIONS = {
    "VRayMtl": VRAYMTL_CONNECTIONS
}

material_context = HouNode.HouNode(hou.node("/mat"))


def create_vray_material(mtl_data, create_uv=True):
    mtl_name = mtl_data['name']

    mtl_builder = material_context.create_node("vray_vop_material")
    mtl_builder.set_name(mtl_name + "_VRayMtlBuilder")

    mtl = None

    for c in mtl_builder.children():
        if c.name() == "vrayMtl":
            if mtl_data['material_type'] != "VRayMtl":
                c.destroy()
                mtl = mtl_builder.create_node(mtl_data['material_type'])
            else:
                mtl = c

    mtl.set_name(mtl_name + "_" + mtl_data['material_type'])

    # Create UV
    if create_uv:
        float_uv_u = mtl_builder.create_node("VRayNodeFloatToTex", "UV_Repeat_U")
        float_uv_v = mtl_builder.create_node("VRayNodeFloatToTex", "UV_Repeat_V")

    for tex_type in mtl_data['textures'].keys():
        if tex_type == "displacement":
            continue

        tex_path = mtl_data['textures'][tex_type]['path']
        use_ptex = mtl_data['textures'][tex_type]['use_ptex']

        # Create file texture node
        tex_node = mtl_builder.create_node("VRayNodeMetaImageFile")
        tex_node.set_name("{}_{}_TEX".format(mtl_name, tex_type))

        # Set tex path
        tex_node.BitmapBuffer_file.set(tex_path)

        # Make connection to mtl
        connections = MTL_CONNECTIONS[mtl_data['material_type']]

        mtl.set_input(connections[tex_type], tex_node)

        if tex_type == "normal":
            mtl.bump_type.set("Normal (Tangent)")

        # Create CC
        cc = create_cc_node(mtl_builder, input_node=tex_node, name=tex_node.name())

        # UV Connection
        if create_uv:
            tex_node.set_input(6, float_uv_u)
            tex_node.set_input(7, float_uv_v)

    mtl_builder.layout_children()


def create_cc_node(parent, input_node=None, name=''):
    if not isinstance(parent, HouNode.HouNode):
        parent = HouNode.HouNode(parent)

    cc = parent.create_node("VRayNodeTexColorCorrect")

    if name:
        name = name + "_CC" if not name.endswith("_CC") else name
        cc.set_name(name)

    if input_node:
        if not isinstance(input_node, HouNode.HouNode):
            input_node = HouNode.HouNode(input_node)

        if input_node.node_type() == "VRayNodeMetaImageFile":
            # Connect CC to original input_node's output
            connections = input_node.output_connections()

            for c in connections:
                if c.outputIndex() == 0:
                    output_node = HouNode.HouNode(c.outputNode())
                    output_node.set_input(c.inputIndex(), cc, 0)
                    break

            # Connect input_node to CC
            cc.set_input(0, input_node, 0)

    return cc
