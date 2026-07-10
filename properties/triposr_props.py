import bpy
from bpy.types import (
    Scene, PropertyGroup
)
from bpy.props import (
    IntProperty, BoolProperty, PointerProperty, EnumProperty
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

    is_transparent_bg: BoolProperty(
        name="Transparent Input",
        description="If true, input images must have a transparent background.\nIf false, input images must have a solid gray (RGB(128 128 128)) colour. Note that if the subject of the image is also gray, the model might fail to distinguish the subject from the background.\nConsider enabling Background Correction and adjust when needed.",
        default=True
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