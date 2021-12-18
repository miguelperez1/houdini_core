import hou as hou


class HouNode(object):
    def __init__(self, houdini_node):
        self.node = houdini_node

        for parm in self.node.parms():
            setattr(self, parm.name(), parm)

    def create_node(self, node_type, name=''):
        node = None
        try:
            n = self.node.createNode(node_type)
        except Exception as e:
            raise e
        else:
            node = HouNode(n)
            if name:
                node.set_name(name)
        finally:
            return node

    def name(self):
        return self.node.name()

    def set_name(self, name):
        self.node.setName(name)

    def children(self):
        return [HouNode(child) for child in self.node.children()]

    def destroy(self):
        self.node.destroy()

    def set_input(self, to_index, node, from_index=0):
        if not getattr(self.node, "setInput"):
            return

        if isinstance(node, HouNode):
            node = node.node

        self.node.setInput(to_index, node, from_index)

    def layout_children(self):
        self.node.layoutChildren()

    def output_connections(self):
        return self.node.outputConnections()

    def node_type(self):
        return self.node.type().name()

    def node_path(self):
        return self.node.path()

    def set_display_flag(self, set):
        self.node.setDisplayFlag(set)

    def set_render_flag(self, set):
        self.node.setRenderFlag(set)
