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

def register():
    bpy.utils.register_class(OpenLRMProps)
    Scene.genai_props_openlrm = PointerProperty(type=OpenLRMProps)

def unregister():
    bpy.utils.unregister_class(OpenLRMProps)
    del Scene.genai_props_openlrm