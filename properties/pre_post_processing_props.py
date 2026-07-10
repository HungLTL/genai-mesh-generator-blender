import bpy
from bpy.types import (
    Scene, PropertyGroup
)
from bpy.props import (
    FloatProperty, IntProperty, BoolProperty, PointerProperty
)

class BackgroundColorCorrectionProps(PropertyGroup):
    bg_correct_enabled: BoolProperty(
        name = "Enable Background Correction",
        description = "If enabled, change the background colour of the input image to the provided RGB values.\nOpenLRM inputs should have a solid white background.\nTripoSR inputs require either a transparent or a solid gray background, depending whether or not Transparent Input is enabled.\nOnly enable this setting if your input does not satisfy the requirements for your selected model.",
        default = False
    )
    r_value: IntProperty(
        name="R",
        default=0,
        min=0,
        max=255
    )
    g_value: IntProperty(
        name="G",
        default=0,
        min=0,
        max=255
    )
    b_value: IntProperty(
        name="B",
        default=0,
        min=0,
        max=255
    )
    a_value: FloatProperty(
        name="A",
        default=1.0,
        min=0,
        max=1.0
    )

class PostMeshRotationProps(PropertyGroup):
    post_gen_rot: BoolProperty(
        name = "Enable Post Generation Rotation",
        description = "If enabled, the output mesh will have extra rotation applied to each respective axis in degrees.",
        default = False
    )
    x_value: FloatProperty(
        name="X",
        default=0.0,
        min=-360.0,
        max=360.0
    )
    y_value: FloatProperty(
        name="Y",
        default=0.0,
        min=-360.0,
        max=360.0
    )
    z_value: FloatProperty(
        name="Z",
        default=0.0,
        min=-360.0,
        max=360.0
    )

classes=[BackgroundColorCorrectionProps, PostMeshRotationProps]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    Scene.genai_props_bg_color = PointerProperty(type=BackgroundColorCorrectionProps)
    Scene.genai_props_post_gen_rot = PointerProperty(type=PostMeshRotationProps)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del Scene.genai_props_bg_color
    del Scene.genai_props_post_gen_rot