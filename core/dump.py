
from dataclasses import asdict
from io import BytesIO
import json
import tarfile
from typing import BinaryIO

from anyio import Any
import cv2
from .report import PredictReport
from micro import CDN


class PredictDumps:
    @staticmethod
    def dump(img, report: PredictReport, proc1: Any, proc2: Any | None, rgb_to_bgr: bool = True) -> BinaryIO:
        buf = BytesIO()

        if rgb_to_bgr:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        with tarfile.open(fileobj=buf, mode='w:gz') as tar:
            img = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 80])[1].tobytes()
            PredictDumps.__add_file(tar, 'img.jpg', img)
            del img
            info = {
                'report': asdict(report),
                'proc1': [(float(area[0]), float(area[1]), float(area[2]), float(area[3]), float(area[4]), int(area[5])) 
                    for area in proc1.xywhn[0]],
                'proc2': [(float(area[0]), float(area[1]), float(area[2]), float(area[3]), float(area[4]), int(area[5]))
                    for area in proc2.xywhn[0]] if proc2 else None
            }
            PredictDumps.__add_file(tar, 'report.json', json.dumps(info).encode('utf-8'))
        buf.seek(0)
        return buf
    
    @staticmethod
    def save(img, des: str, report: PredictReport, proc1: Any, proc2: Any | None) -> str:
        return CDN.upload_file(PredictDumps.dump(img, report, proc1, proc2), 'predict_dump ' + des, 'application/tar+gzip', 3)

    @staticmethod
    def __add_file(tar: tarfile.TarFile, name: str, data: bytes):
        info = tarfile.TarInfo(name=name)
        info.size = len(data)
        tar.addfile(info, fileobj=BytesIO(data))