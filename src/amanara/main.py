from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from amanara.api.router import router

app = FastAPI(
    title="Amanara AI Chatbot API",
    version="1.0.0",
)

app.include_router(router)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/docs")