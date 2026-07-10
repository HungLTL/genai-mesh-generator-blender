import os
import shutil

#from ..backend import TSRInferrer
from ..backend import fetch_and_init_model
from ..utils import convert_image_utils, mesh_utils
from ..utils.file_utils import prepare_working_dir

import bpy
from bpy.types import Operator, Scene

class GenAI_OP_TripoSRToMesh(Operator):
    bl_idname = "genai.triposr_to_mesh"
    bl_label = "Generate Mesh"

    def execute(self, context):
        scene = context.scene
        props = scene.genai_props_triposr
        working_dir = prepare_working_dir()

        image_name = scene.genai_props_image
        image = convert_image_utils.bpy_to_pil(
            image=bpy.data.images[image_name],
            change_background=scene.genai_props_bg_color.bg_correct_enabled,
            r=scene.genai_props_bg_color.r_value,
            g=scene.genai_props_bg_color.g_value,
            b=scene.genai_props_bg_color.b_value,
            a=scene.genai_props_bg_color.a_value
        )

        args_dict = {
            "to_device": "cuda:0",
            "pretrained_model_name_or_path": "stabilityai/TripoSR",
            "chunk_size": props.chunk_size,
            "mc_resolution": props.mc_resolution,
            "output_dir": working_dir,
            "bake_texture": False,
            "texture_resolution": 0,
            "render": False,
            "is_transparent_bg": props.is_transparent_bg
        }
        if scene.genai_model_path:
            args_dict["pretrained_model_name_or_path"] = scene.genai_model_path

        #with TSRInferrer(args_dict=args_dict) as inferrer:
        with fetch_and_init_model(model_id=scene.genai_props_model, args_dict=args_dict) as inferrer:
            mesh_path = inferrer.run(image=image, format=props.output_mesh_format)
            
            if os.path.exists(mesh_path):
                if props.output_mesh_format == 'OPTION_TSR_GLB':
                    bpy.ops.import_scene.gltf(filepath=mesh_path)
                else:
                    bpy.ops.wm.obj_import(filepath=mesh_path)
                if (scene.genai_props_post_gen_rot.post_gen_rot
                    and (scene.genai_props_post_gen_rot.x_value > 0.0
                         or scene.genai_props_post_gen_rot.y_value > 0.0
                         or scene.genai_props_post_gen_rot.z_value > 0.0)):
                    results = context.selected_objects
                    if (len(results) > 0):
                        for mesh in results:
                            mesh_utils.rotate_object(
                                scene.genai_props_post_gen_rot.x_value,
                                scene.genai_props_post_gen_rot.y_value,
                                scene.genai_props_post_gen_rot.z_value,
                                mesh
                            )
                print('Mesh generation finished.')
                #del inferrer
                shutil.rmtree(os.path.dirname(mesh_path))
                return {'FINISHED'}
            else:
                print('Mesh path not found.')
                #del inferrer
                return {'CANCELLED'}
        
def register():
    bpy.utils.register_class(GenAI_OP_TripoSRToMesh)

def unregister():
    bpy.utils.unregister_class(GenAI_OP_TripoSRToMesh)