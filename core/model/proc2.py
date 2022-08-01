from typing import Any, Callable
from .yolov5 import Yolov5


class Proc2(Yolov5):
    def __init__(self, path: str, device: str, agnostic: bool = True) -> None:
        super().__init__(path=path, device=device, agnostic=agnostic)

    def predict(self, img, **args) -> tuple[list[tuple[int, int, int, int, float, str]], Any]:
        pred = super().predict(img, **args)
        xywh = pred.xywh[0]

        return [self.to_pred(area) for area in xywh], pred

    def to_pred(self, area) -> tuple[int, int, int, int, float, str]:
        return (
            int(area[0] - (area[2] / 2)),
            int(area[1] - (area[3] / 2)),
            int(area[2]),
            int(area[3]),
            float(area[4]),
            self.model.names[int(area[5])]  # type: ignore
        )

    def find_best_area(self, areas, filter: Callable[[int, int, float], bool] | None) -> int:
        best_index = -1
        best_loss = -1

        for i, area in enumerate(areas.xywhn[0]):
            if filter != None and not filter(i, int(area[5]), area[4]):
                continue

            xc, yc = area[0], area[1]
            loss = ((abs(.5-xc) + abs(.5-yc))*2 + (1-area[4])) / 2

            if best_index == -1 or loss < best_loss:
                best_index = i
                best_loss = loss
        
        return best_index

    