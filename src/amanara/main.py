from fastapi import FastAPI

from amanara.api.router import api_router
from amanara.config.settings import settings

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

app.include_router(api_router)