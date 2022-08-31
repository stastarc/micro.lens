from fastapi import APIRouter
from . import purchase
from . import query

router = APIRouter(prefix="/billing")

router.include_router(purchase.router)
router.include_router(query.router)