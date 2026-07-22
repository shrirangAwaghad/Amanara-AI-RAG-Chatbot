from amanara.rag.loader import DocumentLoader
from amanara.rag.chunker import TextChunker
from amanara.services.embedding_service import EmbeddingService
from amanara.services.qdrant_service import QdrantService


class IngestionPipeline:
    def __init__(self):
        self.loader = DocumentLoader()
        self.chunker = TextChunker()
        self.embedding_service = EmbeddingService()
        self.qdrant_service = QdrantService()

    def run(self):

        # -----------------------------
        # Load Documents
        # -----------------------------
        print("Loading documents...")
        documents = self.loader.load_documents()
        print(f"Loaded {len(documents)} document(s).")

        if not documents:
            print("No documents found. Ingestion aborted.")
            return

        # -----------------------------
        # Chunk Documents
        # -----------------------------
        print("Chunking documents...")
        chunks = self.chunker.chunk_documents(documents)
        print(f"Generated {len(chunks)} chunk(s).")

        if not chunks:
            print("No chunks generated. Ingestion aborted.")
            return

        # -----------------------------
        # Generate Embeddings
        # -----------------------------
        print("Generating embeddings...")

        embeddings = []

        for index, chunk in enumerate(chunks, start=1):
            embedding = self.embedding_service.embed_text(chunk.text)
            embeddings.append(embedding)

            if index % 50 == 0 or index == len(chunks):
                print(f"Embedded {index}/{len(chunks)} chunks")

        print(f"Generated {len(embeddings)} embedding(s).")

        # -----------------------------
        # Recreate Qdrant Collection
        # (Deletes old vectors)
        # -----------------------------
        print("Recreating Qdrant collection...")
        self.qdrant_service.create_collection()

        # -----------------------------
        # Upload Embeddings
        # -----------------------------
        print("Uploading chunks to Qdrant...")
        self.qdrant_service.upload_chunks(
            chunks=chunks,
            embeddings=embeddings,
        )

        print("Knowledge Base rebuilt successfully.")