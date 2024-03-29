from typing import Any
import cv2

from os.path import join as path_join
from env import Env
from .report import DiseaseReport, PredictReport
from .config import ModelsConfig
from .model import ModelManager
from .dump import PredictDumps
from .model.proc3 import Proc3
from .model.proc2 import Proc2

class Predict:
    config: ModelsConfig
    
    @staticmethod
    def init():
        Predict.config = ModelsConfig.load(path_join(Env.MODELS_DIR, 'config.json'))
        
        for cfg in Predict.config.models:
            ModelManager.register(
                path=cfg.path,
                type=cfg.type,
                autoload=cfg.autoload,
                device=cfg.device
            )
    
    @staticmethod
    def dispose():
        ModelManager.dispose()

    @staticmethod
    def analysis(img, dump: bool = False, des: str | None = None) -> tuple[PredictReport, str] | PredictReport | None:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        proc1_pred = Predict.detect_plant(img)

        if proc1_pred == None: 
            return None
        
        pred, pred_raw = proc1_pred
        x, y, w, h, s, l, = pred
        name, area, = l.split('.')
        disease = Predict.analysis_disease(img[y:y+h, x:x+w], name, area)
        if disease:
            disease, pred2_raw = disease
        else:
            pred2_raw = None

        report = PredictReport(
            score=s,
            name=name,
            area=area,
            rect=(x, y, w, h),
            disease=disease
        )

        if dump:
            return report, PredictDumps.save(img, des, report, pred_raw, pred2_raw)
        
        return report


    @staticmethod
    def detect_plant(img) -> tuple[int, int, int, int, float, str, Any] | None:
        return ModelManager.get('proc.1.pt', autoload=True).predict(img)

    @staticmethod
    def analysis_disease(img, name: str, area: str) -> tuple[DiseaseReport, Any] | None:
        proc3: Proc3 | None = ModelManager.get_safe(f'disease/{name}.{area}.pt', autoload=True)
        
        if proc3 == None:
            return None

        pred: list[tuple[str, float]] = proc3.predict(img, size=512)
        proc2: Proc2 = ModelManager.get('proc.2.pt', autoload=True)
        proc2_pred = proc2.predict(img)
        pub_pred, raw_pub = proc2_pred
        disease, score = max(pred, key=lambda x: x[1])
        assist = proc3.assist[disease]

        if disease == 'healthy':
            if assist['not']:
                n = sum(1 for area in pub_pred if area[-1] in assist['not'])
                if n: score /= n
            
            return DiseaseReport(
                healthy=True,
                name=disease,
                score=score,
                rect=None
            ), raw_pub
        
        if assist['has']:
            pub_filt = [1 if area[-1] in assist['has'] else -1 for area in pub_pred]
            best = proc2.find_best_area(raw_pub, lambda i, l, s: pub_filt[i] == 1)

            n = sum(pub_filt)
            if n > 0: score = (score+n)/(1+n)
            elif n < 0: score /= -n
        else:
            best = proc2.find_best_area(raw_pub, None)

        if best != -1:
            area = pub_pred[best]
            rect = area[:4]
        else:
            rect = None

        return DiseaseReport(
            healthy=False,
            name=disease,
            score=score,
            rect=rect
        ), raw_pub
        