from fastapi.routing import APIRouter
from . import analysis

router = APIRouter(prefix='/lens')

router.include_router(analysis.router)