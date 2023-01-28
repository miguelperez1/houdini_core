import os

import hou as hou

from houdini_core.HouNode import HouNode

VRAYMTL_CONNECTIONS = {
    'diffuse': 0,
    'gloss': 9,
    'normal': 5,
    'specular': 8
}

MTL_CONNECTIONS = {
    "VRayMtl": VRAYMTL_CONNECTIONS
}

material_context = HouNode.HouNode(hou.node("/mat"))


def create_vray_material(mtl_data, create_uv=True):
    mtl_name = mtl_data['material_name']

    mtl_builder = material_context.create_node("vray_vop_material")
    mtl_builder.set_name(mtl_name + "_VRayMtlBuilder")

    mtl = None
    vroutput = None

    for c in mtl_builder.children():
        if c.name() == "vrayMtl":
            if mtl_data['material_shader'] != "VRayMtl":
                c.destroy()
                mtl = mtl_builder.create_node(mtl_data['material_shader'])
            else:
                mtl = c
        elif c.name() == "vrayOutput":
            vroutput = c

    mtl.set_name(mtl_name + "_" + mtl_data['material_shader'])

    # Create UV
    if create_uv:
        float_uv_u = mtl_builder.create_node("VRayNodeFloatToTex", "UV_Repeat_U")
        float_uv_v = mtl_builder.create_node("VRayNodeFloatToTex", "UV_Repeat_V")

    for tex_type, tex_path in mtl_data['textures'].items():
        # Create file texture node
        # TODO PTex check
        tex_node = mtl_builder.create_node("VRayNodeMetaImageFile")
        tex_node.set_name("{}_{}_TEX".format(mtl_name, tex_type))

        # Set tex path
        tex_node.BitmapBuffer_file.set(tex_path)

        # Create CC
        cc = create_cc_node(mtl_builder, input_node=tex_node, name=tex_node.name())

        # UV Connection
        if create_uv:
            tex_node.set_input(6, float_uv_u)
            tex_node.set_input(7, float_uv_v)

        if tex_type == "normal":
            mtl.bump_type.set("Normal(Tangent)")

        if tex_type == "displacement":
            displacement = mtl_builder.create_node("VRayNodeGeomDisplacedMesh", mtl_name + "_DISP")

            displacement.set_input(0, cc)

            vroutput.set_input(1, displacement)

            continue

        # Make connection to mtl
        connections = MTL_CONNECTIONS[mtl_data['material_shader']]

        mtl.set_input(connections[tex_type], cc)

    mtl_builder.layout_children()

    return mtl_builder


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
