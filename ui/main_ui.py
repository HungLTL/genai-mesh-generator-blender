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
        return context.scene.genai_props_model != 'OPTION_DEFAULT' and context.scene.genai_props_model != 'OPTION_EVAL'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.prop(scene, "genai_model_path")
        row.operator(GenAI_OP_Import_HF_Weights.bl_idname)

class GENAI_PT_Main_SubUI_Preprocess_Input(Panel):
    bl_label = "Input Preprocessing"
    bl_idname = "GENAI_PT_Main_SubUI_Preprocess_Input"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GenAI'
    bl_parent_id = 'GENAI_PT_Main'

    @classmethod
    def poll(cls, context):
        return context.scene.genai_props_model != 'OPTION_DEFAULT' and context.scene.genai_props_model != 'OPTION_EVAL'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.genai_props_bg_color

        row = layout.row()
        row.prop(props, "bg_correct_enabled")
        row = layout.row()
        row.prop(props, "r_value")
        row.prop(props, "g_value")
        row.prop(props, "b_value")
        row.prop(props, "a_value")

class GENAI_PT_Main_SubUI_Preprocess_Output(Panel):
    bl_label = "Output Preprocessing"
    bl_idname = "GENAI_PT_Main_SubUI_Preprocess_Output"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GenAI'
    bl_parent_id = 'GENAI_PT_Main'

    @classmethod
    def poll(cls, context):
        return context.scene.genai_props_model != 'OPTION_DEFAULT' and context.scene.genai_props_model != 'OPTION_EVAL'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.genai_props_post_gen_rot

        row = layout.row()
        row.prop(props, "post_gen_rot")
        row = layout.row()
        row.prop(props, "x_value")
        row.prop(props, "y_value")
        row.prop(props, "z_value")

classes=[
    GENAI_PT_Main,
    GENAI_PT_Main_SubUI_Import_Model,
    GENAI_PT_Main_SubUI_Preprocess_Input,
    GENAI_PT_Main_SubUI_Preprocess_Output
]
            
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    