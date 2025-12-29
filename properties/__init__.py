from . import openlrm_props

from bpy.types import Scene
from bpy.props import EnumProperty, StringProperty

def register():
    openlrm_props.register()
    Scene.genai_props_model = EnumProperty(
        name = "Model",
        description = "Select a model for mesh generation.",
        items = (
            ('OPTION_LRM', "OpenLRM", "Use OpenLRM Model"),
            ('OPTION_DEFAULT', "none", "Default Value")
        ),
        default = 'OPTION_DEFAULT'
    )
    Scene.genai_props_image = StringProperty(
        name="Image Name"
    )
    Scene.genai_model_path = StringProperty(
        name = "Model path",
        description = "Path to a model's weights."
    )

def unregister():
    openlrm_props.unregister()
    del Scene.genai_props_model
    del Scene.genai_props_image
    del Scene.genai_model_path