from abc import ABC, abstractmethod

class ModelInferrer(ABC):
    # fetches the model from the repository
    def __init__(self, modelpath=""):
        pass

    # infer the model
    @abstractmethod
    def run(self, image=""):
        pass