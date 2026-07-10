import os
from pathlib import Path
from PIL import Image
from math import radians
import numpy as np

from pytorch3d.io import load_obj, load_ply
from pytorch3d.structures import Meshes
from pytorch3d.ops import sample_points_from_meshes
from pytorch3d.loss import chamfer_distance

from ..utils.file_utils import check_extension, prepare_working_dir, image_exts

import bpy
from bpy.types import Operator
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper

class GenAI_OP_Chamfer_Import_GT(Operator, ImportHelper):
    bl_idname = "genai.chamfer_import_gt"
    bl_label = "Import Ground Truth (Chamfer)"

    filepath: StringProperty(
        name="Mesh Path",
        #default = default_image_dir,
        description="Location of the ground truth mesh.",
        maxlen=1024,
        subtype='FILE_PATH'
    )

    def execute(self, context):
        scene = context.scene
        mesh_path = self.filepath

        if (os.path.exists(mesh_path) and check_extension(mesh_path, [".obj", ".ply"])):
            scene.genai_props_chamfer_distance.ground_truth_path = self.filepath
            return {'FINISHED'}
        else:
            print("Either the path does not exist, or the file type isn't supported!")
            return {'CANCELLED'}

class GenAI_OP_Chamfer_Set_Mesh_Output(Operator):
    bl_idname = "genai.chamfer_output_dir"
    bl_label = "Set Output Directory"

    directory: StringProperty(
        name="Directory Path",
        description="Directory to save the output meshes.",
        maxlen=1024,
        subtype='DIR_PATH'
    )

    @classmethod
    def poll(cls, context):
        return context.scene.genai_props_chamfer_distance.save_output_meshes

    def execute(self, context):
        scene = context.scene
        output_path = self.directory

        if (os.path.isdir(output_path)):
            scene.genai_props_chamfer_distance.save_output_location = output_path
            return {'FINISHED'}
        else:
            print("Output directory does not exist!")
            return {'CANCELLED'}
        
    def invoke(self, context, _event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class GenAI_OP_Chamfer_Eval(Operator):
    bl_idname = "genai.chamfer_eval"
    bl_label = "Evaluate Chamfer Distance"

    def execute(self, context):
        scene = context.scene
        gt_path = scene.genai_props_chamfer_distance.ground_truth_path
        test_meshes = context.selected_objects
        if (len(test_meshes) <= 0):
            print("No meshes selected!")
            return {'CANCELLED'}
        else:
            if (
                context.scene.genai_props_chamfer_distance.save_output_meshes
                and os.path.isdir(context.scene.genai_props_chamfer_distance.save_output_location)):
                working_dir = context.scene.genai_props_chamfer_distance.save_output_location
            else:
                working_dir = prepare_working_dir()

            if ("ply" in os.path.splitext(gt_path)[-1].lower()):
                temp_export_path = os.path.join(working_dir, "temp.ply")
                bpy.ops.wm.ply_export(filepath=temp_export_path, export_selected_objects=True)

                verts, faces, _ = load_ply(scene.genai_props_chamfer_distance.ground_truth_path)
                verts_val, faces_val, _ = load_ply(temp_export_path)
            else:
                temp_export_path = os.path.join(working_dir, "temp.obj")
                bpy.ops.wm.obj_export(filepath=temp_export_path, export_selected_objects=True)

                verts, faces, _ = load_obj(scene.genai_props_chamfer_distance.ground_truth_path)
                verts_val, faces_val, _ = load_obj(temp_export_path)
            
            gt_mesh = Meshes(verts=[verts], faces=[faces.verts_idx])
            val_mesh = Meshes(verts=[verts_val], faces=[faces_val.verts_idx])

            gt_pointcloud = sample_points_from_meshes(gt_mesh, scene.genai_props_chamfer_distance.num_sampling_points)
            val_pointcloud = sample_points_from_meshes(val_mesh, scene.genai_props_chamfer_distance.num_sampling_points)
            loss_chamfer, _ = chamfer_distance(gt_pointcloud, val_pointcloud)
            print("Loss: ", loss_chamfer)
            #print("Loss normals: " + loss_chamfer[1])
            return {'FINISHED'}

class GenAI_OP_PSNR_SSIM_Set_Image_Output(Operator):
    bl_idname = "genai.psnr_ssim_set_output"
    bl_label = "Set Output Directory"

    directory: StringProperty(
        name="Directory Path",
        description="Directory to save the output images.",
        maxlen=1024,
        subtype='DIR_PATH'
    )

    def execute(self, context):
        scene = context.scene
        output_path = self.directory

        if (os.path.isdir(output_path)):
            scene.genai_props_psnr_ssim.save_output_location = output_path
            return {'FINISHED'}
        else:
            print("Output directory does not exist!")
            return {'CANCELLED'}
        
    def invoke(self, context, _event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class GenAI_OP_PSNR_SSIM_Take_Photo(Operator):
    bl_idname = "genai.psnr_ssim_take_photo"
    bl_label = "Take Photo"

    def execute(self, context):
        scene = context.scene
        working_dir = scene.genai_props_psnr_ssim.save_output_location
        if (os.path.isdir(working_dir)):
            if scene.genai_props_psnr_ssim.photo_mode == 'OPTION_PSNR_SSIM_VAL':
                img_path = os.path.join(working_dir, scene.genai_props_psnr_ssim.val_name + ".png")
            else:
                img_path = os.path.join(working_dir, scene.genai_props_psnr_ssim.ground_truth_name + ".png")
            
            scene.render.filepath = img_path
            scene.render.film_transparent = True
            bpy.ops.render.render(write_still=True)
            return {'FINISHED'}
        else:
            print("The provided output directory does not exist!")
            return {'CANCELLED'}
        
class GenAI_OP_PSNR_SSIM_Eval(Operator):
    bl_idname = "genai.psnr_ssim_eval"
    bl_label = "Evaluate PSNR and SSIM"

    def execute(self, context):
        scene = context.scene
        working_dir = context.scene.genai_props_psnr_ssim.save_output_location
        gt_name = scene.genai_props_psnr_ssim.ground_truth_name
        val_name = scene.genai_props_psnr_ssim.val_name

        if (os.path.isdir(working_dir)):
            gt_path = os.path.join(working_dir, gt_name + ".png")
            val_path = os.path.join(working_dir, val_name + ".png")
            if (os.path.isfile(gt_path) and os.path.isfile(val_path)):
                gt_img = np.asarray(Image.open(gt_path))
                val_img = np.asarray(Image.open(val_path))
                if (gt_img.shape == val_img.shape):
                    from skimage.metrics import peak_signal_noise_ratio, structural_similarity
                    psnr = peak_signal_noise_ratio(gt_img, val_img)
                    ssim = structural_similarity(gt_img, val_img, channel_axis = 2)
                    print("PSNR: " + str(psnr))
                    print("SSIM: " + str(ssim))
                    return {'FINISHED'}
                else:
                    print("Image shape mismatch!")
                    return {'CANCELLED'}
            else:
                print("One of the provided files, or both, do not exist or are invalid!")
                print(gt_path)
                print(val_path)
                return {'CANCELLED'}
        else:
            print("The provided directory does not exist!")
            return {'CANCELLED'}
        
class GenAI_OP_IoU_Eval(Operator):
    bl_idname = "genai.iou_eval"
    bl_label = "Evaluate IoU"

    def execute(self, context):
        scene = context.scene
        gt_name = scene.genai_props_iou.mesh_name_gr
        val_name = scene.genai_props_iou.mesh_name_eval

        mesh_gt = scene.objects.get(gt_name)
        mesh_eval = scene.objects.get(val_name)

        if mesh_gt and mesh_eval:
            import trimesh
            from ..utils.mesh_utils import blender_mesh_to_trimesh
            mesh1 = blender_mesh_to_trimesh(mesh_gt)
            mesh2 = blender_mesh_to_trimesh(mesh_eval)

            try:
                intersection = trimesh.boolean.intersection(meshes=[mesh1, mesh2],engine='blender').volume
                union = trimesh.boolean.union(meshes=[mesh1, mesh2],engine='blender').volume

                iou = intersection / union if union > 0 else 0.0
                print("IoU: " + str(iou))
                return {'FINISHED'}
            except Exception as e:
                print("Boolean operation failed; switching to voxel-based method instead")
                from ..utils.mesh_utils import compute_iou_voxel
                iou = compute_iou_voxel(mesh_gt, mesh_eval, scene.genai_props_iou.voxel_size)
                print("IoU: " + str(iou))
                return {'FINISHED'}
        else:
            print("Cannot find a mesh with the provided names in the scene!")
            return {'CANCELLED'}

classes=[
    GenAI_OP_Chamfer_Import_GT,
    GenAI_OP_Chamfer_Set_Mesh_Output,
    GenAI_OP_Chamfer_Eval,
    GenAI_OP_PSNR_SSIM_Set_Image_Output,
    GenAI_OP_PSNR_SSIM_Take_Photo,
    GenAI_OP_PSNR_SSIM_Eval,
    GenAI_OP_IoU_Eval
]
            
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)