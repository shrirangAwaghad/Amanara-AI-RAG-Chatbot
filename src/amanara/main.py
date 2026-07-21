from fastapi import FastAPI
from amanara.config.settings import settings

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "environment": settings.app_env,
    }
    