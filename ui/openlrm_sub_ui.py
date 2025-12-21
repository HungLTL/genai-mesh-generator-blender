import bpy
from bpy.types import Panel

from ..operators import openlrm_operators

class GENAI_PT_OpenLRM(Panel):
    bl_label = "OpenLRM"
    bl_idname = "GENAI_PT_OpenLRM"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GenAI'
    bl_parent_id = 'GENAI_PT_Main'

    @classmethod
    def poll(cls, context):
        return context.scene.genai_props_model == 'OPTION_LRM'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.genai_props_openlrm
        
        row = layout.row()
        row.prop(props, "source_size")
        row = layout.row()
        row.prop(props, "source_cam_dist")
        row = layout.row()
        row.prop(props, "frame_size")

        row = layout.row()
        row.prop(props, "render_size")
        row = layout.row()
        row.prop(props, "render_views")
        row = layout.row()
        row.prop(props, "render_fps")

        row = layout.row()
        row.prop(props, "mesh_size")
        row = layout.row()
        row.prop(props, "mesh_thres")
        
        row = layout.row()
        row.operator(openlrm_operators.GenAI_OP_OpenLRM_Import_Model_Config.bl_idname)
        row = layout.row()
        row.operator(openlrm_operators.GenAI_OP_OpenLRMToMesh.bl_idname)

class GENAI_PT_ModelLRM(Panel):
    bl_label = "OpenLRM"
    bl_idname = "GENAI_PT_ModelLRM"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GenAI'
    bl_parent_id = 'GENAI_PT_OpenLRM'

    @classmethod
    def poll(cls, context):
        return context.scene.genai_props_model == 'OPTION_LRM'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.genai_props_modellrm
        
        row = layout.row()
        row.prop(props, "camera_embed_dim")
        row = layout.row()
        row.prop(props, "rendering_samples_per_ray")
        row = layout.row()
        row.prop(props, "transformer_dim")

        row = layout.row()
        row.prop(props, "transformer_layers")
        row = layout.row()
        row.prop(props, "transformer_heads")
        row = layout.row()
        row.prop(props, "triplane_low_res")

        row = layout.row()
        row.prop(props, "triplane_high_res")
        row = layout.row()
        row.prop(props, "triplane_dim")
        row = layout.row()
        row.prop(props, "encoder_type")
        row = layout.row()
        row.prop(props, "encoder_model_name")
        row = layout.row()
        row.prop(props, "encoder_feat_dim")
        row = layout.row()
        row.prop(props, "encoder_freeze")
        
        row = layout.row()
        row.operator(openlrm_operators.GenAI_OP_OpenLRM_Import_Model_Config.bl_idname)


def register():
    bpy.utils.register_class(GENAI_PT_OpenLRM)
    bpy.utils.register_class(GENAI_PT_ModelLRM)

def unregister():
    bpy.utils.unregister_class(GENAI_PT_OpenLRM)
    bpy.utils.unregister_class(GENAI_PT_ModelLRM)
