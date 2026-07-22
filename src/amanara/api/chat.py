from fastapi import APIRouter
from pydantic import BaseModel

from amanara.services.gemini_service import GeminiService

router = APIRouter(prefix="/chat", tags=["Chat"])

gemini_service = GeminiService()


class ChatRequest(BaseModel):
    prompt: str


class ChatResponse(BaseModel):
    response: str


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    response = gemini_service.generate_response(request.prompt)
    return ChatResponse(response=response)