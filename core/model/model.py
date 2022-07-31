
from multiprocessing import Lock
from typing import Any


class Model:
    path: str
    loaded: bool
    load_lock: Lock  # type: ignore

    def __init__(self, path: str) -> None:
        self.load_lock = Lock()
        self.path = path
        self.loaded = False

    def load(self):
        with self.load_lock:
            if not self.loaded:
                self._load()

    def predict(self, img, **args) -> Any | None:
        raise NotImplementedError()
    
    
    def _load(self):
        raise NotImplementedError()

    def dispose(self):
        pass

    def __del__(self):
        self.dispose()
    