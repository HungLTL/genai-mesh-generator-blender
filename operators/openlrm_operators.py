import os
import shutil

from omegaconf import OmegaConf

from ..backend import OpenLRMInferrer
from ..utils import convert_image_utils

import bpy
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper

class GenAI_OP_OpenLRM_Import_Config(Operator, ImportHelper):
    bl_idname = "genai.import_configs_openlrm"
    bl_label = "Import configs"

    def execute(self, context):
        yaml_path = self.filepath
        if (os.path.exists(yaml_path) and os.path.splitext(yaml_path)[-1].lower() == ".yaml"):
            scene = context.scene
            props = scene.genai_props_openlrm

            conf = OmegaConf.load(yaml_path)
            if conf.source_size is not None:
                props.source_size = conf.source_size
            if conf.render_size is not None:
                props.render_size = conf.render_size
            if conf.render_views is not None:
                props.render_views = conf.render_views
            if conf.render_fps is not None:
                props.render_fps = conf.render_fps
            if conf.frame_size is not None:
                props.frame_size = conf.frame_size
            if conf.mesh_size is not None:
                props.mesh_size = conf.mesh_size
            if conf.mesh_thres is not None:
                props.mesh_thres = conf.mesh_thres
            if conf.source_cam_dist is not None:
                props.source_cam_dist = conf.source_cam_dist
            return {'FINISHED'}
        else:
            print("Provided path isn't a .yaml file!")
            return {'CANCELLED'}
        
class GenAI_OP_OpenLRM_Import_Model_Config(Operator, ImportHelper):
    bl_idname = "genai.import_configs_modellrm"
    bl_label = "Import model configs"

    def execute(self, context):
        yaml_path = self.filepath
        if (os.path.exists(yaml_path) and os.path.splitext(yaml_path)[-1].lower() == ".yaml"):
            scene = context.scene
            props = scene.genai_props_modellrm

            conf = OmegaConf.load(yaml_path)
            if conf.model.camera_embed_dim is not None:
                props.camera_embed_dim = conf.model.camera_embed_dim
            if conf.model.rendering_samples_per_ray is not None:
                props.rendering_samples_per_ray = conf.model.rendering_samples_per_ray
            if conf.model.transformer_dim is not None:
                props.transformer_dim = conf.model.transformer_dim
            if conf.model.transformer_layers is not None:
                props.transformer_layers = conf.model.transformer_layers
            if conf.model.transformer_heads is not None:
                props.transformer_heads = conf.model.transformer_heads
            if conf.model.triplane_low_res is not None:
                props.triplane_low_res = conf.model.triplane_low_res
            if conf.model.triplane_high_res is not None:
                props.triplane_high_res = conf.model.triplane_high_res
            if conf.model.triplane_dim is not None:
                props.triplane_dim = conf.model.triplane_dim
            if conf.model.encoder_freeze is not None:
                props.encoder_freeze = conf.model.encoder_freeze
            if conf.model.encoder_type is not None:
                props.encoder_type = conf.model.encoder_type
            if conf.model.encoder_model_name is not None:
                props.encoder_model_name = conf.model.encoder_model_name
            if conf.model.encoder_feat_dim is not None:
                props.encoder_feat_dim = conf.model.encoder_feat_dim
            return {'FINISHED'}
        else:
            print("Provided path isn't a .yaml file!")
            return {'CANCELLED'}

class GenAI_OP_OpenLRMToMesh(Operator):
    bl_idname = "genai.openlrm_to_mesh"
    bl_label = "Generate Mesh"
    
    def execute(self, context):
        scene = context.scene
        props = scene.genai_props_openlrm
        model_props = scene.genai_props_modellrm
        model_path = scene.genai_model_path
        args_dict = {
            "model_name": "zxhezexin/openlrm-mix-base-1.1",
            "source_size": props.source_size,
            "source_cam_dist": props.source_cam_dist,
            "frame_size": props.frame_size,
            "render_size": props.render_size,
            "render_views": props.render_views,
            "render_fps": props.render_fps,
            "mesh_size": props.mesh_size,
            "mesh_thres": props.mesh_thres
        }
        config_dict = {
            "camera_embed_dim": model_props.camera_embed_dim,
            "rendering_samples_per_ray": model_props.rendering_samples_per_ray,
            "transformer_dim": model_props.transformer_dim,
            "transformer_layers": model_props.transformer_layers,
            "transformer_heads": model_props.transformer_heads,
            "triplane_low_res": model_props.triplane_low_res,
            "triplane_high_res": model_props.triplane_high_res,
            "triplane_dim": model_props.triplane_dim,
            "encoder_freeze": model_props.encoder_freeze,
            "encoder_type": model_props.encoder_type,
            "encoder_model_name": model_props.encoder_model_name,
            "encoder_feat_dim": model_props.encoder_feat_dim
        }

        inferrer = OpenLRMInferrer(args_dict=args_dict, config_dict=config_dict,modelpath=model_path)
        image_name = scene.genai_props_image
        image = convert_image_utils.bpy_to_pil(bpy.data.images[image_name])

        # debug_path = "E:\\blender projects\\New folder\\output"
        mesh_path = inferrer.run(image=image)
        if os.path.exists(mesh_path):
            bpy.ops.wm.ply_import(filepath = mesh_path)
            print('Mesh generation finished.')
            del inferrer
            shutil.rmtree(os.path.dirname(mesh_path))
            return {'FINISHED'}
        else:
            print('Mesh path not found.')
            del inferrer
            return {'CANCELLED'}

classes=[GenAI_OP_OpenLRM_Import_Config, GenAI_OP_OpenLRM_Import_Model_Config, GenAI_OP_OpenLRMToMesh]
            
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)