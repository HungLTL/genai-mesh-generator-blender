import os

image_exts = [".jpeg", ".jpg", ".png", ".bmp", ".webp"]
model_exts = [".pt", ".pth", ".ckpt", ".h5", ".onnx", ".safetensors", ".gguf", ".tflite", ".engine", ".mlmodel"]

def check_extension(filename: str, extensions_list):
    return (os.path.splitext(filename)[-1].lower() in extensions_list)

def prepare_working_dir():
    import tempfile
    working_dir = tempfile.mkdtemp()
    return working_dir