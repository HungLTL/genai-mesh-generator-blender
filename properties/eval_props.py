import bpy
from bpy.types import (
    Scene, PropertyGroup
)
from bpy.props import (
    IntProperty, StringProperty, PointerProperty, FloatProperty, EnumProperty, BoolProperty
)

class ChamferDistanceProps(PropertyGroup):
    ground_truth_path: StringProperty(
        name="Path to ground truth mesh",
        description="Path to the ground truth mesh file for comparison. The file must either be in .obj or .ply format."
    )
    num_sampling_points: IntProperty(
        name="Number of Sampling Points",
        description="Determines the number of points that will be sampled from the mesh's surface to create a point cloud. The bigger the number, the more accurate the point cloud would be at the cost of potential performance.",
        min=10,
        default=5000
    )
    save_output_meshes: BoolProperty(
        name = "Save Meshes",
        description = "Chamfer Distance calculation requires the validation mesh to be exported first. If this setting is set to True, the validation mesh will be exported to a folder of your choosing; False will have it exported to a temp folder and deleted once testing is done.",
        default = False
    )
    save_output_location: StringProperty(
        name = "Output Mesh Location",
        description = "Only used if Save Meshes is true. Output meshes will be saved into this folder."
    )

class ImageQualityProps(PropertyGroup):
    save_output_location: StringProperty(
        name = "Image Directory",
        description = "When taking pictures, the images will be saved into this directory. When calculating PSNR and SSIM, the validation and ground truth images will be from this directory."
    )
    val_name: StringProperty(
        name = "Val Name",
        description="When taking pictures, the validation image will be saved under this name. When calculating PSNR and SSIM, the Image Directory folder must have an image with this name."
    )
    ground_truth_name: StringProperty(
        name = "GT Name",
        description="When taking pictures, the ground truth image will be saved under this name. When calculating PSNR and SSIM, the Image Directory folder must have an image with this name."
    )
    photo_mode: EnumProperty(
        name = "Photo Mode",
        description = "Is the photo being taken of the ground truth or validation mesh?",
        items = (
            ('OPTION_PSNR_SSIM_GT', "Ground truth", "Take Ground Truth Image"),
            ('OPTION_PSNR_SSIM_VAL', "Validation", "Take Validation Image")
        ),
        default = 'OPTION_PSNR_SSIM_GT'
    )

class IoUProps(PropertyGroup):
    mesh_name_gr: StringProperty(
        name = "Ground Truth",
        description = "The name of the ground truth mesh in the scene."
    )
    mesh_name_eval: StringProperty(
        name = "Evaluating Mesh",
        description = "The name of the mesh in the scene that needs evaluation."
    )
    voxel_size: FloatProperty(
        name = "Voxel Size",
        description = "If voxelization is needed, this determines the size of the voxel grid. A smaller voxel size will give more accurate results, at the expense of speed.",
        default = 0.1
    )

classes=[ChamferDistanceProps, ImageQualityProps, IoUProps]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    Scene.genai_props_chamfer_distance = PointerProperty(type=ChamferDistanceProps)
    Scene.genai_props_psnr_ssim = PointerProperty(type=ImageQualityProps)
    Scene.genai_props_iou = PointerProperty(type=IoUProps)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del Scene.genai_props_chamfer_distance
    del Scene.genai_props_psnr_ssim
    del Scene.genai_props_iou