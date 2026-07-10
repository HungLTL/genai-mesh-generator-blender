import bpy
from bpy.types import Panel

from ..operators import triposr_operators

class GENAI_PT_TripoSR(Panel):
    bl_label = "TripoSR"
    bl_idname = "GENAI_PT_TripoSR"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GenAI'
    bl_parent_id = 'GENAI_PT_Main'

    @classmethod
    def poll(cls, context):
        return context.scene.genai_props_model == 'OPTION_TSR'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.genai_props_triposr
        
        row = layout.row()
        row.prop(props, "chunk_size")
        row = layout.row()
        row.prop(props, "mc_resolution")
        row = layout.row()
        row.prop(props, "output_mesh_format")
        row = layout.row()
        row.prop(props, "is_transparent_bg")
        row = layout.row()
        row.operator(triposr_operators.GenAI_OP_TripoSRToMesh.bl_idname)

def register():
    bpy.utils.register_class(GENAI_PT_TripoSR)

def unregister():
    bpy.utils.unregister_class(GENAI_PT_TripoSR)