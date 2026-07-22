from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from amanara.config.settings import settings
from qdrant_client.models import PointStruct
from uuid import uuid4

from amanara.models.chunk import Chunk

class QdrantService:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )

    def create_collection(self):
        self.client.recreate_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=VectorParams(
                size=3072,
                distance=Distance.COSINE,
            ),
        )

        print(f"Collection '{settings.qdrant_collection}' created successfully.")
    
    def upload_chunks(
        self,
        chunks: list[Chunk],
        embeddings: list[list[float]],
    ):
        points = []

        for chunk, embedding in zip(chunks, embeddings):
            points.append(
                PointStruct(
                    id=str(uuid4()),
                    vector=embedding,
                    payload={
                        "text": chunk.text,
                        "source": chunk.source,
                        "document_id": chunk.document_id,
                        "chunk_id": chunk.chunk_id,
                    },
                )
            )

        self.client.upsert(
            collection_name=settings.qdrant_collection,
            points=points,
        )

        print(f"Uploaded {len(points)} chunks.")
    
    def search(self, embedding: list[float], top_k: int = 5):
        results = self.client.query_points(
            collection_name=settings.qdrant_collection,
            query=embedding,
            limit=top_k,
            with_payload=True,
        )

        return results.points
    
    