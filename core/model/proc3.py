import json
import os
from typing import Any
from .classifier import Classifier


class Proc3(Classifier):
    labels: list[str]
    assist: dict[str, Any]

    def __init__(self, path: str, device: str) -> None:
        super().__init__(path, device)
        file = os.path.splitext(path)[0]
        label_path = file + '.json'

        if not os.path.exists(label_path):
            raise FileNotFoundError(f'label file {label_path} not found')
        
        with open(label_path) as f:
            cfg = json.load(f)
            self.labels = cfg['labels']
            self.assist = cfg['assist']
        

    def predict(self, img, **args) -> list[float] | list[tuple[str, float]] | None:
        scores = super().predict(img, **args)

        if scores == None:
            return None

        if not args.get('labeling', True):
            return [float(score) for score in scores]
        
        return [(self.labels[i], float(score)) for i, score in enumerate(scores)]
