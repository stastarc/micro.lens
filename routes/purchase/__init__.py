from fastapi import APIRouter
from . import purchase

router = APIRouter(prefix="/billing")

router.include_router(purchase.router)