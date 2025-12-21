import bpy
from bpy.types import (
    Scene, PropertyGroup
)
from bpy.props import (
    FloatProperty, IntProperty, BoolProperty, StringProperty, PointerProperty
)

class OpenLRMProps(PropertyGroup):
    source_size: IntProperty(
        name="Source Size",
        default=336,
        min=0
    )

    render_size: IntProperty(
        name="Render Size",
        default=288,
        min=0
    )

    render_views: IntProperty(
        name="Render Views",
        default=100,
        min=0
    )

    render_fps: IntProperty(
        name="Render FPS",
        default=25,
        min=0
    )

    frame_size: IntProperty(
        name="Frame Size",
        default=2,
        min=0
    )

    mesh_size: IntProperty(
        name="Mesh Size",
        default=384,
        min=0
    )

    mesh_thres: FloatProperty(
        name="Mesh Threshold",
        default=3.0,
        min=0
    )

    source_cam_dist: FloatProperty(
        name="Source Camera Distance",
        default=2.0,
        min=0
    )

class ModelLRMProps(PropertyGroup):
    camera_embed_dim: IntProperty(
        name="Camera Embedding Dimension",
        default=1024,
        min=0
    )

    rendering_samples_per_ray: IntProperty(
        name="Rendering Samples per Ray",
        default=96,
        min=0
    )

    transformer_dim: IntProperty(
        name="Transformer Dimension",
        default=512,
        min=0
    )

    transformer_layers: IntProperty(
        name="Transformer Layers",
        default=12,
        min=0
    )

    transformer_heads: IntProperty(
        name="Transformer Heads",
        default=8,
        min=0
    )

    triplane_low_res: IntProperty(
        name="Triplane Lowest Resolution",
        default=32,
        min=0
    )

    triplane_high_res: IntProperty(
        name="Triplane Highest Resolution",
        default=64,
        min=0
    )

    triplane_dim: IntProperty(
        name="Triplane Dimensions",
        default=32,
        min=0
    )

    encoder_freeze: BoolProperty(
        name = "Encoder Freeze",
        default = False
    )

    encoder_type: StringProperty(
        name = "Encoder Type",
        default = "dinov2"
    )

    encoder_model_name: StringProperty(
        name = "Encoder Model Name",
        default = "dinov2_vits14_reg"
    )

    encoder_feat_dim: IntProperty(
        name="Encoder Feature Dimensions",
        default=384,
        min=0
    )

def register():
    bpy.utils.register_class(OpenLRMProps)
    bpy.utils.register_class(ModelLRMProps)
    Scene.genai_props_openlrm = PointerProperty(type=OpenLRMProps)
    Scene.genai_props_modellrm = PointerProperty(type=ModelLRMProps)

def unregister():
    bpy.utils.unregister_class(OpenLRMProps)
    bpy.utils.unregister_class(ModelLRMProps)
    del Scene.genai_props_openlrm
    del Scene.genai_props_modellrm