import os
from pathlib import Path
from PIL import Image

from ..utils.file_utils import prepare_working_dir
from .fetch_model import ModelInferrer
from ..models.triposr.tsr.infer import TripoSRInferrer

class TSRInferrer(ModelInferrer):
    def __init__(self, args_dict):
        super().__init__(args_dict=args_dict)
        #self.args_dict = args_dict

        # self.output_dir = args_dict['output_dir']
        # os.makedirs(self.output_dir, exist_ok=True)

    def run(self, image: Image, format: str):
        working_dir = prepare_working_dir()
        if format == "OPTION_TSR_GLB":
            dump_mesh_path = Path(os.path.join(working_dir, "output.glb"))
        else:
            dump_mesh_path = Path(os.path.join(working_dir, "output.obj"))
        
        with TripoSRInferrer(args_dict=self.args_dict) as inferrer:
            inferrer.infer_single(index=0,image=image,path=dump_mesh_path)
            return str(dump_mesh_path)
    
    def __exit__(self, exc_type, exc_value, traceback):
        import gc
        del self.args_dict
        gc.collect()