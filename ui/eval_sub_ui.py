import bpy
from bpy.types import Panel

from ..operators import eval_operators

class GENAI_PT_Eval_Chamfer(Panel):
    bl_label = "Evaluation: Chamfer Distance"
    bl_idname = "GENAI_PT_Eval_Chamfer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GenAI'
    bl_parent_id = 'GENAI_PT_Main'

    @classmethod
    def poll(cls, context):
        return context.scene.genai_props_model == 'OPTION_EVAL'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.genai_props_chamfer_distance
        gt_path = props.ground_truth_path
        
        row = layout.row()
        label_text = "No ground truth selected" if ((not gt_path) or (gt_path == "")) else gt_path
        row.label(text=label_text)
        row.operator(eval_operators.GenAI_OP_Chamfer_Import_GT.bl_idname)
        row = layout.row()
        row.prop(props, "num_sampling_points")

        row = layout.row()
        row.prop(props, "save_output_meshes")
        row = layout.row()
        row.prop(props, "save_output_location")
        row.operator(eval_operators.GenAI_OP_Chamfer_Set_Mesh_Output.bl_idname)

        row = layout.row()
        row.operator(eval_operators.GenAI_OP_Chamfer_Eval.bl_idname)

class GENAI_PT_Eval_PSNR_SSIM(Panel):
    bl_label = "Evaluation: PSNR and SSIM"
    bl_idname = "GENAI_PT_Eval_PSNR_SSIM"

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GenAI'
    bl_parent_id = 'GENAI_PT_Main'

    @classmethod
    def poll(cls, context):
        return context.scene.genai_props_model == 'OPTION_EVAL'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.genai_props_psnr_ssim

        row = layout.row()
        row.prop(props, "save_output_location")
        row.operator(eval_operators.GenAI_OP_PSNR_SSIM_Set_Image_Output.bl_idname)

        row = layout.row()
        row.prop(props, "val_name")
        row = layout.row()
        row.prop(props, "ground_truth_name")
        row = layout.row()
        row.prop(props, "photo_mode")
        row = layout.row()
        row.operator(eval_operators.GenAI_OP_PSNR_SSIM_Take_Photo.bl_idname)

        row = layout.row()
        row.operator(eval_operators.GenAI_OP_PSNR_SSIM_Eval.bl_idname)

class GENAI_PT_Eval_IoU(Panel):
    bl_label = "Evaluation: IoU"
    bl_idname = "GENAI_PT_Eval_IoU"

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GenAI'
    bl_parent_id = 'GENAI_PT_Main'

    @classmethod
    def poll(cls, context):
        return context.scene.genai_props_model == 'OPTION_EVAL'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.genai_props_iou

        row = layout.row()

        row = layout.row()
        row.prop(props, "mesh_name_gr")
        row = layout.row()
        row.prop(props, "mesh_name_eval")
        row = layout.row()
        row.prop(props, "voxel_size")

        row = layout.row()
        row.operator(eval_operators.GenAI_OP_IoU_Eval.bl_idname)

classes = [
    GENAI_PT_Eval_Chamfer,
    GENAI_PT_Eval_PSNR_SSIM,
    GENAI_PT_Eval_IoU
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)