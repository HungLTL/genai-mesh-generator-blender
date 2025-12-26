from abc import ABC, abstractmethod

class ModelInferrer(ABC):
    # fetches the model from the repository
    def __init__(self, modelpath=""):
        pass

    def __enter__(self):
        return self

    def __exit__(self):
        pass

    # infer the model
    @abstractmethod
    def run(self, image=""):
        pass