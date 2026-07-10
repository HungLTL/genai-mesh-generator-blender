import struct
import numpy as np
from PIL import Image

import bpy

def valid_rgb(x: int):
    return (x <= 255 and x >= 0)

def valid_rgb_alpha(a: float):
    return (a <= 1.0 and a >= 0.0)

def pil_to_bpy(image: Image, name='NewImage'):
    width, height = image.width, image.height
    normalized = 1.0 / 255.0
    bpy_image = bpy.data.images.new(name, width=width, height=height)
    bpy_image.pixels[:] = (np.asarray(image.convert('RGBA'), dtype=np.float32) * normalized).ravel()
    return bpy_image

def bpy_to_pil(image: bpy.types.Image, change_background: False, r: 0, g: 0, b: 0, a: 1.0):
    pixels = [int(px * 255) for px in image.pixels[:]]
    bytes = struct.pack("%sB" % len(pixels), *pixels)
    pil_image = Image.frombytes('RGBA', (image.size[0], image.size[1]), bytes)

    if (change_background):
        assert valid_rgb(r) and valid_rgb(g) and valid_rgb(b) and valid_rgb_alpha(a), "Provided RGB value is out of bounds!"
        background = Image.new(mode="RGBA",size=pil_image.size,color=(r, g, b))
        if (a < 1.0):
            background.putalpha(int((256 * a) - 1))
        background.paste(pil_image, (0, 0), pil_image)
        return background
    else:
        return pil_image
