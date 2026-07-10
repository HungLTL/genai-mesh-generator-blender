import os
import torch
from pathlib import Path
from PIL import Image

from ..utils.file_utils import prepare_working_dir
from .fetch_model import ModelInferrer
from ..models.craftsman3d.craftsman import CraftsManPipeline

class CraftsManInferrer(ModelInferrer):
    def __init__(self, args_dict, modelpath=""):
        super().__init__(args_dict=args_dict)
        #self.args_dict = args_dict
        self.model_path = modelpath
        self.inferrer = CraftsManPipeline.from_pretrained(
            modelpath,
            device="cuda:0",
            torch_dtype=torch.bfloat16,
            num_inference_steps=args_dict['num_inference_steps'],
            guidance_scale=args_dict['guidance_scale'],
            eta=args_dict['eta']
        )

    def run(self, image: Image, path=""):
        output_name = ""
        if self.args_dict['output_type'] == 'OPTION_CRAFTSMAN_OBJ':
            output_name = "output.obj"
        else:
            output_name = "output.glb"

        if not path:
            working_dir = prepare_working_dir()
            dump_mesh_path = Path(os.path.join(working_dir, output_name))
        else:
            dump_mesh_path = os.path.join(path, output_name)

        with CraftsManPipeline.from_pretrained(
            self.model_path,
            device="cuda:0",
            torch_dtype=torch.bfloat16,
            num_inference_steps=self.args_dict['num_inference_steps'],
            guidance_scale=self.args_dict['guidance_scale'],
            eta=self.args_dict['eta']
        ) as inferrer:
            inferrer(
                image=image,
                foreground_ratio=self.args_dict['foreground_ratio'],
                mc_depth=self.args_dict['mc_depth'],
                only_max_component=self.args_dict['only_max_component']
            ).meshes[0].export(dump_mesh_path)
            print(f"Mesh path: {dump_mesh_path}")
            return str(dump_mesh_path)
    
    def __exit__(self, exc_type, exc_value, traceback):
        import gc
        del self.args_dict
        del self.model_path
        gc.collect()
