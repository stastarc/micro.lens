
from dataclasses import dataclass


@dataclass
class DiseaseReport:
    healthy: bool
    name: str
    score: float
    rect: tuple[int, int, int, int] | None

@dataclass
class PredictReport:
    score: float
    name: str
    area: str
    rect: tuple[int, int, int, int]
    disease: DiseaseReport | None