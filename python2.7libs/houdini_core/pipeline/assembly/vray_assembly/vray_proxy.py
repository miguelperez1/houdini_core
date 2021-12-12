import os
import logging

import hou as hou

from HouNode.HouNode import HouNode

obj_context = HouNode(hou.node("/obj"))


def create_vray_proxy(path, material, name=''):
    geo = obj_context.create_node("geo")

    if name:
        geo.set_name(name)

    proxy = geo.create_node("VRayNodeVRayProxy")
    proxy.file.set(path)
