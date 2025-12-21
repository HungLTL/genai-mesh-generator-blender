bl_info = {
    "name": "GenAI Mesh",
    "author": "Lê Trường Long Hưng",
    "version": (2, 0),
    "blender": (4, 4, 0),
    "location": "View3D > Add > Mesh > GenAI > New Object",
    "description": "Open-source integrated 3D Mesh Generator for Blender using generative AI models.",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}

import bpy

from . import properties
from . import operators
from . import ui

def register():
    properties.register()
    operators.register()
    ui.register()

def unregister():
    properties.unregister()
    operators.unregister()
    ui.unregister()


if __name__ == "__main__":
    register()