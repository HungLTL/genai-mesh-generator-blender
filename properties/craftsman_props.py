import bpy
from bpy.types import (
    Scene, PropertyGroup
)
from bpy.props import (
    FloatProperty, IntProperty, BoolProperty, EnumProperty, PointerProperty
)

class CraftsmanProps(PropertyGroup):
    num_inference_steps: IntProperty(
        name="Inference Steps",
        description="The number of denoising steps. More denoising steps usually lead to a higher quality image at the expense of slower inference. Default: 15",
        default=15,
        min=1
    )

    guidance_scale: FloatProperty(
        name="Guidance Scale",
        description="Enabled by setting a value higher than 1.0. A higher guidance scale will encourage the model to generate images closer to the text prompt, at the cost of image quality. Default: 7.5f",
        default=7.5,
        min=0.0
    )

    eta: FloatProperty(
        name="ETA",
        description="Only used with the DDIM scheduler. Controls the amount of noise added to the latent space.",
        default=0.0,
        min=0.0,
        max=1.0
    )

    foreground_ratio: FloatProperty(
        name="Foreground Ratio",
        description="The ratio of the foreground in the image. The foreground is the part of the image that is not the background. The foreground is resized to the size of the background image while maintaining the aspect ratio. The background is filled with black color.",
        default=1.0,
        min=0.0,
        max=1.0
    )

    mc_depth: IntProperty(
        name="Marching Cubes Depth",
        description="The resolution of the Marching Cubes algorithm. The resolution is the number of cubes in the x, y, and z. 8 means 2^8 = 256 cubes in each dimension. The higher the resolution, the more detailed the mesh will be. Default: 8",
        default=8,
        min=0
    )

    only_max_component: BoolProperty(
        name = "Only Max Component",
        description="Whether to only keep the largest connected component of the mesh. This is useful when the mesh has multiple components and only the largest one is needed. Default: False",
        default = False
    )

    output_type: EnumProperty(
        name = "Output",
        description = "Output format of mesh. Default: .glb",
        items = (
            ('OPTION_CRAFTSMAN_OBJ', ".obj", "Model will return an .obj file."),
            ('OPTION_CRAFTSMAN_GLB', ".glb", "Model will return a .glb file.")
        ),
        default = 'OPTION_CRAFTSMAN_GLB'
    )

def register():
    bpy.utils.register_class(CraftsmanProps)
    Scene.genai_props_craftsman = PointerProperty(type=CraftsmanProps)

def unregister():
    bpy.utils.unregister_class(CraftsmanProps)
    del Scene.genai_props_craftsman