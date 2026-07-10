import os
from pathlib import Path
from PIL import Image

from ..utils.file_utils import prepare_working_dir
from .fetch_model import ModelInferrer
from ..models.openlrm.runners.infer import LRMInferrer

class OpenLRMInferrer(ModelInferrer):
    def __init__(self, args_dict, modelpath=""):
        super().__init__(args_dict=args_dict)
        #self.args_dict = args_dict
        self.model_path = modelpath

    def run(self, image: Image, path=""):
        if not path:
            working_dir = prepare_working_dir()
            dump_mesh_path = Path(os.path.join(working_dir, "output.ply"))
        else:
            dump_mesh_path = os.path.join(path, "output.ply")

        print(f"Mesh path: {dump_mesh_path}")
        with LRMInferrer(self.args_dict, self.model_path) as inferrer:
            inferrer.infer_single(image,source_cam_dist=None,dump_mesh_path=dump_mesh_path)
            return str(dump_mesh_path)
    
    def __exit__(self, exc_type, exc_value, traceback):
        import gc
        del self.model_path
        del self.args_dict
        gc.collect()
        #import gc
        #del self.inferrer
        #torch.cuda.memory.empty_cache()
        #gc.collect()
        