import bpy
from bpy.types import Panel

from ..operators.general_operators import GenAI_OP_Import_Image, GenAI_OP_Import_HF_Weights

class GENAI_PT_Main(Panel):
    bl_label = "Main"
    bl_idname = "GENAI_PT_Main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GenAI'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        image_name = scene.genai_props_image

        row = layout.row()
        label_text = "No image selected" if ((not image_name) or (image_name == "")) else image_name
        row.label(text=label_text)
        row.operator(GenAI_OP_Import_Image.bl_idname)
        row = layout.row()
        row.prop(scene, "genai_props_model")

class GENAI_PT_Main_SubUI_Import_Model(Panel):
    bl_label = "Import Model"
    bl_idname = "GENAI_PT_Main_SubUI_Import_Model"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GenAI'
    bl_parent_id = 'GENAI_PT_Main'

    @classmethod
    def poll(cls, context):
        return context.scene.genai_props_model != 'OPTION_DEFAULT'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.prop(scene, "genai_model_path")
        row.operator(GenAI_OP_Import_HF_Weights.bl_idname)

classes=[GENAI_PT_Main, GENAI_PT_Main_SubUI_Import_Model]
            
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    