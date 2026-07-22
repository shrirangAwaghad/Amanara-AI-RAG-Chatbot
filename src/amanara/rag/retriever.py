from amanara.services.embedding_service import EmbeddingService
from amanara.services.qdrant_service import QdrantService


class Retriever:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.qdrant_service = QdrantService()

    def retrieve(self, query: str, top_k: int = 5):
        query_embedding = self.embedding_service.embed_text(query)
        results = self.qdrant_service.search(
            embedding=query_embedding,
            top_k=top_k,
        )

        return results