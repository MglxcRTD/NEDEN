class FSNode:
    """Clase base para cualquier elemento del sistema de archivos."""
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

class File(FSNode):
    """Representa un archivo con contenido de texto."""
    def __init__(self, name, content="", parent=None):
        super().__init__(name, parent)
        self.content = content

class Directory(FSNode):
    """Representa un directorio que puede contener otros nodos."""
    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self.children = {}

    def add_node(self, node):
        self.children[node.name] = node

    def remove_node(self, name):
        if name in self.children:
            del self.children[name]
            return True
        return False

    def get_node(self, name):
        return self.children.get(name)