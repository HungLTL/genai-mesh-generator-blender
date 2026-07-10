from . import openlrm_props, triposr_props, craftsman_props, pre_post_processing_props, eval_props

from bpy.types import Scene
from bpy.props import EnumProperty, StringProperty

def register():
    Scene.genai_props_model = EnumProperty(
        name = "Model",
        description = "Select a model for mesh generation.",
        items = (
            ('OPTION_LRM', "OpenLRM", "Use OpenLRM Model"),
            ('OPTION_CFT3D', "CraftsMan3D", "Use CraftsMan3D Model"),
            ('OPTION_TSR', "TripoSR", "Use TripoSR Model"),
            ('OPTION_DEFAULT', "none", "No model selected"),
            ('OPTION_EVAL', "Evaluate", "Evaluate generated meshes")
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

    openlrm_props.register()
    craftsman_props.register()
    triposr_props.register()
    pre_post_processing_props.register()
    eval_props.register()

def unregister():
    eval_props.unregister()
    pre_post_processing_props.unregister()
    openlrm_props.unregister()
    craftsman_props.unregister()
    triposr_props.unregister()
    del Scene.genai_props_model
    del Scene.genai_props_image
    del Scene.genai_model_path