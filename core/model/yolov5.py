from typing import Any
import yolov5
from yolov5.models.common import DetectMultiBackend, AutoShape
from .model import Model


class Yolov5(Model):
    device: str
    model: DetectMultiBackend | AutoShape
    agnostic: bool

    def __init__(self, path: str, device: str, agnostic: bool = False) -> None:
        super().__init__(path)
        self.device = device
        self.agnostic = agnostic
        self.model = None

    def _load(self):
        self.model = yolov5.load(self.path, device=self.device)
        self.model.agnostic = self.agnostic
        self.loaded = True
    
    def predict(self, img, **args) -> Any | None:
        return self.model(img)
    
    def dispose(self):
        try:
            if self.model:
                del self.model.model
        except: pass
        self.loaded = False