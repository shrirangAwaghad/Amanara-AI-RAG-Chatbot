from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from amanara.config.settings import settings
from qdrant_client.models import PointStruct
from uuid import uuid4
import uuid
from amanara.models.chunk import Chunk

class QdrantService:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )

    def create_collection(self):
        collection_name = settings.qdrant_collection
        if self.client.collection_exists(collection_name):
            print(f"Collection '{collection_name}' already exists.")
            return

        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=3072,
                distance=Distance.COSINE,
            ),
        )

        print(f"Collection '{collection_name}' created successfully.")

    def recreate_collection(self):
        """Delete and recreate the collection to remove stale vectors."""
        collection_name = settings.qdrant_collection

        if self.client.collection_exists(collection_name):
            self.client.delete_collection(collection_name)
            print(f"Deleted existing collection '{collection_name}'.")

        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=3072,
                distance=Distance.COSINE,
            ),
        )

        print(f"Collection '{collection_name}' recreated successfully.")

    def upload_chunks(
        self,
        chunks: list[Chunk],
        embeddings: list[list[float]],
    ):
        if len(chunks) != len(embeddings):
            raise ValueError(
                f"Chunks and embeddings count mismatch: "
                f"{len(chunks)} chunks, {len(embeddings)} embeddings."
                )
        points = []

        for chunk, embedding in zip(chunks, embeddings):
            points.append(
                PointStruct(
                    id=str(uuid.uuid5(
                        uuid.NAMESPACE_URL,
                        f"{chunk.source}:{chunk.chunk_id}",
                        )
                    ),
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
