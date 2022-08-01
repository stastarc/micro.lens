from fastapi.routing import APIRouter
from . import analysis

router = APIRouter(prefix='/search')

router.include_router(analysis.router)