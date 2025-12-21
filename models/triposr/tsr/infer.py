import os
import torch
# import rembg
import numpy as np

# from PIL import Image
from omegaconf import OmegaConf

from ...base_inferrer import Inferrer
from .system import TSR


def parse_configs(args_dict):
    assert args_dict, "Cannot pass an empty set of arguments!"

    args = OmegaConf.create(args_dict)
    args.setdefault('to-device', 'cuda:0')
    args.setdefault('pretrained-model-name-or-path', 'stabilityai/TripoSR')

    return args


class TripoSRInferrer(Inferrer):
    EXP_TYPE: str = 'tsr'

    def __init__(self, args_dict):
        super().__init__()

        self.args = parse_configs(args_dict)

        self.device = self.args.to_device
        if not torch.cuda.is_available():
            self.device = "cpu"

        self.model = self._build_model(self.args.pretrained_model_name_or_path, self.args.chunk_size).to(self.device)

    def _build_model(self, pretrained_model_name_or_path, chunk_size):
        model = TSR.from_pretrained(
            pretrained_model_name_or_path,
            config_name="config.yaml",
            weight_name="model.ckpt",
        )
        model.renderer.set_chunk_size(chunk_size)
        return model

    def infer_single(self, index, image, path):
        # if self.args.no_remove_bg:
        image = np.array(image.convert("RGB"))
        # else:
            # rembg_session = rembg.new_session()

            # image = remove_background(image, rembg_session)
            # image = resize_foreground(image, args.foreground_ratio)
            # image = np.array(image).astype(np.float32) / 255.0
            # image = image[:, :, :3] * image[:, :, 3:4] + (1 - image[:, :, 3:4]) * 0.5
            # image = Image.fromarray((image * 255.0).astype(np.uint8))
        
        with torch.no_grad():
            scene_codes = self.model([image], device=self.device)
        
        meshes = self.model.extract_mesh(scene_codes, not self.args.bake_texture, resolution=self.args.mc_resolution)
        meshes[0].export(path)

    def infer(self):
        outputs = []
        for index, path in enumerate(self.args.image):
            output_path = self.infer_single(self, index, path, self.args)
            outputs.append(output_path)
        
        return outputs