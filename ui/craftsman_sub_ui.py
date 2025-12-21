import bpy
from bpy.types import Panel

from ..operators import craftsman_operators

class GENAI_PT_Craftsman(Panel):
    bl_label = "CraftsMan3D"
    bl_idname = "GENAI_PT_Craftsman"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GenAI'
    bl_parent_id = 'GENAI_PT_Main'

    @classmethod
    def poll(cls, context):
        return context.scene.genai_props_model == 'OPTION_CFT3D'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.genai_props_craftsman
        
        row = layout.row()
        row.prop(props, "num_inference_steps")
        row = layout.row()
        row.prop(props, "guidance_scale")
        row = layout.row()
        row.prop(props, "eta")

        row = layout.row()
        row.prop(props, "foreground_ratio")
        row = layout.row()
        row.prop(props, "mc_depth")
        row = layout.row()
        row.prop(props, "only_max_component")
        row = layout.row()
        row.prop(props, "output_type")

        row = layout.row()
        row.operator(craftsman_operators.GenAI_OP_CraftsMan_Import_Config.bl_idname)
        row = layout.row()
        row.operator(craftsman_operators.GenAI_OP_CraftsmanToMesh.bl_idname)

def register():
    bpy.utils.register_class(GENAI_PT_Craftsman)

def unregister():
    bpy.utils.unregister_class(GENAI_PT_Craftsman)