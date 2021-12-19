import hou as hou

from houdini_core.HouNode import HouNode

obj_context = hou.node("/obj")

VRAY_LIGHT_TYPES = {
    "VRayNodeLightAmbient": "color_tex",
    "VRayNodeLightMesh": "color_tex",
    "VRayNodeLightRectangle": "rect_tex",
    "VRayNodeLightIES": "ies_file",
    "VRayNodeLightSphere": "color_tex",
    "VRayNodeLightDome": "dome_tex",
    "VRayNodeLightSpot": "color_tex",
    "VRayNodeLightDirect": "color_tex",
    "VRayNodeSunLight": None
}


def create_vray_light(light_type, path=None, name=None):
    if light_type not in VRAY_LIGHT_TYPES.keys():
        return

    light = HouNode.HouNode(obj_context.createNode(light_type))

    if name:
        light.set_name(name.replace("Node", ""))

    if path:
        getattr(light, VRAY_LIGHT_TYPES[light_type]).set(path)

    light.invisible.set(1)

    if light_type == "VRayNodeLightRectangle" and path:
        light.rect_tex_multiply_by_color.set(1)
    elif light_type == "VRayNodeLightDome" and path:
        light.dome_tex_multiply_by_color.set(1)
        light.dome_spherical.set(1)
        light.dome_adaptive.set(1)

    return light
