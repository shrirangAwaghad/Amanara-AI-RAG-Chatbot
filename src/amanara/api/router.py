from fastapi import APIRouter

from amanara.api.health import router as health_router
from amanara.api.chat import router as chat_router

router = APIRouter()

router.include_router(health_router)
router.include_router(chat_router)