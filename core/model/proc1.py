from typing import Any
from .yolov5 import Yolov5


class Proc1(Yolov5):
    def __init__(self, path: str, device: str, agnostic: bool = True) -> None:
        super().__init__(path=path, device=device, agnostic=agnostic)

    def predict(self, img, **args) -> tuple[int, list[tuple[int, int, int, int, float, str]], Any] | tuple[int, int, int, int, float, str, Any] | None:
        pred = super().predict(img, **args)

        if pred == None or not len(pred.xywh[0]):
            return None

        xywh = pred.xywh[0]
        xywhn = pred.xywhn[0]
        best = Proc1.find_best_area(xywhn)

        if args.get('best_only', True):

            if best == -1:
                return None

            return self.to_pred(xywh[best]), pred
        
        return best, [self.to_pred(area) for area in xywh], pred

    def to_pred(self, area) -> tuple[int, int, int, int, float, str]:
        return (
            int(area[0] - (area[2] / 2)),
            int(area[1] - (area[3] / 2)),
            int(area[2]),
            int(area[3]),
            float(area[4]),
            self.model.names[int(area[5])]  # type: ignore
        )

    @staticmethod
    def find_best_area(areas) -> int:
        best_index = -1
        best_loss = -1

        for i, area in enumerate(areas):
            xc, yc = area[0], area[1]
            w, h = area[2], area[3]
            loss = (w + h + abs(.5-xc) + abs(.5-yc) + (1-area[4])) / 4

            if best_index == -1 or loss < best_loss:
                best_index = i
                best_loss = loss
        
        return best_index

    