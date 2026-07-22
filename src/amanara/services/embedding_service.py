
    
from google import genai

from amanara.config.settings import settings


class EmbeddingService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.google_api_key)

    def embed_text(self, text: str) -> list[float]:
        response = self.client.models.embed_content(
            model=settings.embedding_model,
            contents=text,
        )

        return response.embeddings[0].values