import os
import shutil

from omegaconf import OmegaConf

from ..backend import CraftsManInferrer
from ..utils import convert_image_utils

import bpy
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper

class GenAI_OP_CraftsMan_Import_Config(Operator, ImportHelper):
    bl_idname = "genai.import_configs_craftsman"
    bl_label = "Import configs"

    def execute(self, context):
        yaml_path = self.filepath
        if (os.path.exists(yaml_path) and os.path.splitext(yaml_path)[-1].lower() == ".yaml"):
            scene = context.scene
            props = scene.genai_props_craftsman

            conf = OmegaConf.load(yaml_path)
            if conf.system.num_inference_steps is not None:
                props.num_inference_steps = conf.system.num_inference_steps
            if conf.system.guidance_scale is not None:
                props.guidance_scale = conf.system.guidance_scale
            if conf.system.eta is not None:
                props.eta = conf.system.eta
            return {'FINISHED'}
        else:
            print("Provided path isn't a .yaml file!")
            return {'CANCELLED'}
        
class GenAI_OP_CraftsmanToMesh(Operator):
    bl_idname = "genai.craftsman_to_mesh"
    bl_label = "Generate Mesh"

    def execute(self, context):
        scene = context.scene
        props = scene.genai_props_craftsman
        model_path = scene.genai_model_path
        args_dict = {
            "model_name": model_path,
            "num_inference_steps": props.num_inference_steps,
            "guidance_scale": props.guidance_scale,
            "eta": props.eta,
            "foreground_ratio": props.foreground_ratio,
            "mc_depth": props.mc_depth,
            "only_max_component": props.only_max_component,
            "output_type": props.output_type
        }

        with CraftsManInferrer(args_dict=args_dict,modelpath=model_path) as inferrer:
            image_name = scene.genai_props_image
            image = convert_image_utils.bpy_to_pil(bpy.data.images[image_name])

            # debug_path = "E:\\blender projects\\New folder\\output"
            mesh_path = inferrer.run(image=image)
            if os.path.exists(mesh_path):
                if props.output_type == 'OPTION_CRAFTSMAN_OBJ':
                    bpy.ops.wm.obj_import(filepath = mesh_path)
                else:
                    bpy.ops.import_scene.gltf(filepath = mesh_path)
                print('Mesh generation finished.')
                #del inferrer
                shutil.rmtree(os.path.dirname(mesh_path))
                return {'FINISHED'}
            else:
                print('Mesh path not found.')
                #del inferrer
                return {'CANCELLED'}

classes=[GenAI_OP_CraftsMan_Import_Config, GenAI_OP_CraftsmanToMesh]
            
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)