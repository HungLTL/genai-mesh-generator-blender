import bpy
from bpy.types import (
    Scene, PropertyGroup
)
from bpy.props import (
    FloatProperty, IntProperty, BoolProperty, PointerProperty, EnumProperty
)

class TripoSRProps(PropertyGroup):
    chunk_size: IntProperty(
        name="Chunk Size",
        description="Evaluation chunk size for surface extraction and rendering. Smaller chunk size reduces VRAM usage but increases computation time. 0 for no chunking. Default: 8192",
        default=8192,
        min=0
    )

    mc_resolution: IntProperty(
        name="Marching Cubes Grid Resolution",
        description="Default: 256",
        default=256,
        min=0
    )

    output_mesh_format: EnumProperty(
        name = "Output Format",
        description = "Format to save the generated mesh. Default: obj.",
        items = (
            ('OPTION_TSR_OBJ', ".obj", "Export to .obj"),
            ('OPTION_TSR_GLB', ".glb", "Export to glob")
        ),
        default = 'OPTION_TSR_OBJ'
    )

def register():
    bpy.utils.register_class(TripoSRProps)
    Scene.genai_props_triposr = PointerProperty(type=TripoSRProps)

def unregister():
    bpy.utils.unregister_class(TripoSRProps)
    del Scene.genai_props_triposr