
from dataclasses import dataclass
import json


@dataclass
class DiseaseConfig:
    pass

@dataclass
class ModelConfig:
    path: str
    type: str
    device: str | None = None
    autoload: bool = False

@dataclass
class ModelsConfig:
    models: list[ModelConfig]
    disease: DiseaseConfig

    @staticmethod
    def load(path: str) -> 'ModelsConfig':
        with open(path, 'r') as f:
            cfg = ModelsConfig(**json.load(f))
        
        for i, model in enumerate(cfg.models):
            cfg.models[i] = ModelConfig(**model)  # type: ignore
        
        cfg.disease = DiseaseConfig(**cfg.disease)  # type: ignore
        
        return cfg