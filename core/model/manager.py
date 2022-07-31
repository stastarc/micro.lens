
from multiprocessing import Lock
from os.path import join as path_join
from env import Env
from .classifier import Classifier
from .proc1 import Proc1
from .proc2 import Proc2
from .proc3 import Proc3
from .yolov5 import Yolov5
from .model import Model


MODELS: dict[str, type] = {
    'yolov5': Yolov5,
    'classifier': Classifier,
    'proc1': Proc1,
    'proc2': Proc2,
    'proc3': Proc3,
}

class ModelManager:
    models: dict[str, Model] = {}
    lock = Lock()

    @staticmethod
    def register(path: str, type: str, autoload: bool = False, *kwargs, **args) -> Model:
        with ModelManager.lock:
            m = ModelManager.models.get(path, None)

            if m != None:
                return m

            model = MODELS.get(type, None)

            if not model:
                raise ValueError(f'Unknown model type: {type}')

            args['path'] = ModelManager.real_path(path)
            m = model(*kwargs, **args)
            ModelManager.models[path] = m

        if autoload:
            print(f'Loading model: {path}')
            m.load()

        return m

    @staticmethod
    def get(path: str, autoload: bool = False) -> Model:
        model = ModelManager.get_safe(path, autoload)

        if model == None:
            raise ValueError(f'Model not found: {path}')
            
        return model

    @staticmethod
    def get_safe(path: str, autoload: bool = False) -> Model | None:
        with ModelManager.lock:
            model = ModelManager.models.get(path, None)

            if model == None:
                return None

        if autoload and not model.loaded:
            model.load()
        
        return model

    @staticmethod
    def real_path(path: str) -> str:
        return path_join(Env.MODELS_DIR, path)

    @staticmethod
    def dispose():
        with ModelManager.lock:
            for model in ModelManager.models.values():
                del model
            ModelManager.models.clear()