from typing import Any
import yolov5
from yolov5.models.common import DetectMultiBackend, AutoShape
from .model import Model

import torch
import numpy as np
import torch.nn.functional as F
import torchvision.transforms.functional as TF

IMAGENET_MEAN = 0.485, 0.456, 0.406
IMAGENET_STD = 0.229, 0.224, 0.225

def normalize(x, mean=IMAGENET_MEAN, std=IMAGENET_STD):
    return TF.normalize(x, mean, std, inplace=True)

class Classifier(Model):
    model: Any
    device: torch.device

    def __init__(self, path: str, device: str) -> None:
        super().__init__(path)
        self.device = torch.device('cpu') # gpu not supported :(
        self.model = None

    def _load(self):
        self.model = torch.load(self.path, map_location=self.device)['model'].float()
        self.loaded = True
    
    def predict(self, img, **args) -> Any | None:
        size = args.get('size', None) or 512
        resize = torch.nn.Upsample(size=(size, size), mode='bilinear', align_corners=False)
        im = np.ascontiguousarray(np.asarray(img).transpose((2, 0, 1)))
        im = torch.tensor(im).float().unsqueeze(0) / 255.0
        im = resize(im)
        results = self.model(normalize(im))

        return F.softmax(results, dim=1)[0]
    
    def dispose(self):
        if self.model:
            del self.model
        self.loaded = False