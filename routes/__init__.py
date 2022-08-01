from fastapi import FastAPI
from . import internal, lens

def include(app: FastAPI):
    app.include_router(internal.router)
    app.include_router(lens.router)
