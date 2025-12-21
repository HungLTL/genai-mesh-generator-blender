import os

from ..utils.file_utils import check_extension, image_exts

import bpy
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty

class GenAI_OP_Import_Image(Operator, ImportHelper):
    bl_idname = "genai.import"
    bl_label = "Import Image"

    def execute(self, context):
        scene = context.scene
        image_path = self.filepath

        if (os.path.exists(image_path) and check_extension(image_path, image_exts)):
            image = bpy.data.images.load(self.filepath)
            scene.genai_props_image = image.name
            return {'FINISHED'}
        else:
            return {'CANCELLED'}
        
class GenAI_OP_Import_HF_Weights(Operator):
    bl_idname = "genai.hf_import_weights"
    bl_label = "Import HuggingFace Model Weights"

    directory: StringProperty(
        name="Directory Path",
        description="Directory containing a subfolder system storing the model",
        maxlen=1024,
        subtype='DIR_PATH',
    )

    def execute(self, context):
        scene = context.scene
        model_path = self.directory

        if (os.path.isdir(model_path)):
            scene.genai_model_path = model_path
            return {'FINISHED'}
        else:
            return {'CANCELLED'}
        
    def invoke(self, context, _event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

classes=[GenAI_OP_Import_Image, GenAI_OP_Import_HF_Weights]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)