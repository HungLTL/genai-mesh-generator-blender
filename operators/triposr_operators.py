import os
import shutil

from ..backend import TSRInferrer
from ..utils import convert_image_utils
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
        image = convert_image_utils.bpy_to_pil(bpy.data.images[image_name])

        args_dict = {
            "to_device": "cuda:0",
            "pretrained_model_name_or_path": "stabilityai/TripoSR",
            "chunk_size": props.chunk_size,
            "mc_resolution": props.mc_resolution,
            "output_dir": working_dir,
            "bake_texture": False,
            "texture_resolution": 0,
            "render": False
        }
        if scene.genai_model_path:
            args_dict["pretrained_model_name_or_path"] = scene.genai_model_path

        inferrer = TSRInferrer(args_dict=args_dict)
        mesh_path = inferrer.run(image=image, format=props.output_mesh_format)
        
        if os.path.exists(mesh_path):
            if props.output_mesh_format == 'OPTION_TSR_GLB':
                bpy.ops.import_scene.gltf(filepath=mesh_path)
            else:
                bpy.ops.wm.obj_import(filepath=mesh_path)
            print('Mesh generation finished.')
            del inferrer
            shutil.rmtree(os.path.dirname(mesh_path))
            return {'FINISHED'}
        else:
            print('Mesh path not found.')
            del inferrer
            return {'CANCELLED'}
        
def register():
    bpy.utils.register_class(GenAI_OP_TripoSRToMesh)

def unregister():
    bpy.utils.unregister_class(GenAI_OP_TripoSRToMesh)