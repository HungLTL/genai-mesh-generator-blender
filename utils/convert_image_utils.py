import struct
import numpy as np
from PIL import Image

import bpy

def pil_to_bpy(image: Image, name='NewImage'):
    width, height = image.width, image.height
    normalized = 1.0 / 255.0
    bpy_image = bpy.data.images.new(name, width=width, height=height)
    bpy_image.pixels[:] = (np.asarray(image.convert('RGBA'), dtype=np.float32) * normalized).ravel()
    return bpy_image

def bpy_to_pil(image: bpy.types.Image):
    pixels = [int(px * 255) for px in image.pixels[:]]
    bytes = struct.pack("%sB" % len(pixels), *pixels)
    pil_image = Image.frombytes('RGBA', (image.size[0], image.size[1]), bytes)
    return pil_image
