# Copyright (c) 2023-2024, Zexin He
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import torch
import os
import argparse
import mcubes
import trimesh
import numpy as np
from PIL import Image
from omegaconf import OmegaConf
from tqdm.auto import tqdm
from accelerate.logging import get_logger

from ....base_inferrer import Inferrer
from ...datasets.cam_utils import build_camera_principle, create_intrinsics
from ...utils.logging import configure_logger
from ...runners import REGISTRY_RUNNERS
from ...utils.hf_hub import wrap_model_hub


logger = get_logger(__name__)


def parse_configs():

    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str)
    parser.add_argument('--infer', type=str)
    args, unknown = parser.parse_known_args()

    cfg = OmegaConf.create()
    cli_cfg = OmegaConf.from_cli(unknown)

    # parse from ENV
    if os.environ.get('APP_INFER') is not None:
        args.infer = os.environ.get('APP_INFER')
    if os.environ.get('APP_MODEL_NAME') is not None:
        cli_cfg.model_name = os.environ.get('APP_MODEL_NAME')

    if args.config is not None:
        cfg_train = OmegaConf.load(args.config)
        cfg.source_size = cfg_train.dataset.source_image_res
        cfg.render_size = cfg_train.dataset.render_image.high
        _relative_path = os.path.join(cfg_train.experiment.parent, cfg_train.experiment.child, os.path.basename(cli_cfg.model_name).split('_')[-1])
        cfg.video_dump = os.path.join("exps", 'videos', _relative_path)
        cfg.mesh_dump = os.path.join("exps", 'meshes', _relative_path)

    if args.infer is not None:
        cfg_infer = OmegaConf.load(args.infer)
        cfg.merge_with(cfg_infer)
        cfg.setdefault('video_dump', os.path.join("dumps", cli_cfg.model_name, 'videos'))
        cfg.setdefault('mesh_dump', os.path.join("dumps", cli_cfg.model_name, 'meshes'))

    cfg.merge_with(cli_cfg)

    """
    [required]
    model_name: str
    image_input: str
    export_video: bool
    export_mesh: bool

    [special]
    source_size: int
    render_size: int
    video_dump: str
    mesh_dump: str

    [default]
    render_views: int
    render_fps: int
    mesh_size: int
    mesh_thres: float
    frame_size: int
    logger: str
    """

    cfg.setdefault('logger', 'INFO')

    # assert not (args.config is not None and args.infer is not None), "Only one of config and infer should be provided"
    assert cfg.model_name is not None, "model_name is required"
    return cfg

def parse_configs(args_dict):
    assert args_dict, "Cannot pass an empty set of arguments!"

    cfg = OmegaConf.create(args_dict)
    assert cfg.model_name is not None, "model_name is required"
    cfg.setdefault('mesh_dump', os.path.join("dumps", args_dict["model_name"], 'meshes'))
    cfg.setdefault('logger', 'INFO')

    return cfg


@REGISTRY_RUNNERS.register('infer.lrm')
class LRMInferrer(Inferrer):

    EXP_TYPE: str = 'lrm'

    def __init__(self):
        super().__init__()

        self.cfg = parse_configs()
        configure_logger(
            stream_level=self.cfg.logger,
            log_level=self.cfg.logger,
        )

        self.model = self._build_model(self.cfg).to(self.device)

    def __init__(self, args_dict, model_path=""):
        super().__init__()

        self.cfg = parse_configs(args_dict)
        configure_logger(
            stream_level=self.cfg.logger,
            log_level=self.cfg.logger,
        )

        # if (preload == True and preload_path != "" and os.path.exists(preload_path)):
            # self.model = self._build_model(preload_path, config_dict).to(self.device)
        # else:
            # self.model = self._build_model(self.cfg).to(self.device)
        if os.path.isdir(model_path):
            self.model = self._build_model_path(model_path=model_path).to(self.device)
        else:
            self.model = self._build_model(self.cfg).to(self.device)

    def _build_model_path(self, model_path: str):
        from ...models import model_dict
        hf_model_cls = wrap_model_hub(model_dict[self.EXP_TYPE])
        model = hf_model_cls.from_pretrained(pretrained_model_name_or_path=model_path, local_files_only=True)
        return model
    
    def _build_model(self, cfg):
        from openlrm.models import model_dict
        hf_model_cls = wrap_model_hub(model_dict[self.EXP_TYPE])
        model = hf_model_cls.from_pretrained(cfg.model_name)
        return model

    def _default_source_camera(self, dist_to_center: float = 2.0, batch_size: int = 1, device: torch.device = torch.device('cpu')):
        # return: (N, D_cam_raw)
        canonical_camera_extrinsics = torch.tensor([[
            [1, 0, 0, 0],
            [0, 0, -1, -dist_to_center],
            [0, 1, 0, 0],
        ]], dtype=torch.float32, device=device)
        canonical_camera_intrinsics = create_intrinsics(
            f=0.75,
            c=0.5,
            device=device,
        ).unsqueeze(0)
        source_camera = build_camera_principle(canonical_camera_extrinsics, canonical_camera_intrinsics)
        return source_camera.repeat(batch_size, 1)

    # def _default_render_cameras(self, n_views: int, batch_size: int = 1, device: torch.device = torch.device('cpu')):
        # return: (N, M, D_cam_render)
        # render_camera_extrinsics = surrounding_views_linspace(n_views=n_views, device=device)
        # render_camera_intrinsics = create_intrinsics(
            # f=0.75,
            # c=0.5,
            # device=device,
        # ).unsqueeze(0).repeat(render_camera_extrinsics.shape[0], 1, 1)
        # render_cameras = build_camera_standard(render_camera_extrinsics, render_camera_intrinsics)
        # return render_cameras.unsqueeze(0).repeat(batch_size, 1, 1)

    def infer_planes(self, image: torch.Tensor, source_cam_dist: float):
        N = image.shape[0]
        source_camera = self._default_source_camera(dist_to_center=source_cam_dist, batch_size=N, device=self.device)
        planes = self.model.forward_planes(image, source_camera)
        assert N == planes.shape[0]
        return planes

    def infer_mesh(self, planes: torch.Tensor, mesh_size: int, mesh_thres: float, dump_mesh_path: str):
        grid_out = self.model.synthesizer.forward_grid(
            planes=planes,
            grid_size=mesh_size,
        )
        
        vtx, faces = mcubes.marching_cubes(grid_out['sigma'].squeeze(0).squeeze(-1).cpu().numpy(), mesh_thres)
        vtx = vtx / (mesh_size - 1) * 2 - 1

        vtx_tensor = torch.tensor(vtx, dtype=torch.float32, device=self.device).unsqueeze(0)
        vtx_colors = self.model.synthesizer.forward_points(planes, vtx_tensor)['rgb'].squeeze(0).cpu().numpy()  # (0, 1)
        vtx_colors = (vtx_colors * 255).astype(np.uint8)
        
        mesh = trimesh.Trimesh(vertices=vtx, faces=faces, vertex_colors=vtx_colors)

        # dump
        os.makedirs(os.path.dirname(dump_mesh_path), exist_ok=True)
        mesh.export(dump_mesh_path)

    def infer_single(self, image: Image, source_cam_dist: float, dump_mesh_path: str):
        source_size = self.cfg.source_size
        mesh_size = self.cfg.mesh_size
        mesh_thres = self.cfg.mesh_thres
        source_cam_dist = self.cfg.source_cam_dist if source_cam_dist is None else source_cam_dist

        # prepare image: [1, C_img, H_img, W_img], 0-1 scale
        image = torch.from_numpy(np.array(image)).to(self.device)
        image = image.permute(2, 0, 1).unsqueeze(0) / 255.0
        if image.shape[1] == 4:  # RGBA
            image = image[:, :3, ...] * image[:, 3:, ...] + (1 - image[:, 3:, ...])
        image = torch.nn.functional.interpolate(image, size=(source_size, source_size), mode='bicubic', align_corners=True)
        image = torch.clamp(image, 0, 1)

        with torch.no_grad():
            planes = self.infer_planes(image, source_cam_dist=source_cam_dist)

            results = {}
            mesh = self.infer_mesh(planes, mesh_size=mesh_size, mesh_thres=mesh_thres, dump_mesh_path=dump_mesh_path)
            results.update({
                'mesh': mesh,
            })

    def infer(self):
        pass