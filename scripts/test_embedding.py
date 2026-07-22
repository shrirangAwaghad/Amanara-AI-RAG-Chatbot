from amanara.rag.loader import DocumentLoader
from amanara.rag.chunker import TextChunker
from amanara.services.embedding_service import EmbeddingService


loader = DocumentLoader()
documents = loader.load_documents()

chunker = TextChunker(
    chunk_size=500,
    chunk_overlap=100,
)

chunks = chunker.chunk_documents(documents)

embedding_service = EmbeddingService()

print(f"Total Chunks: {len(chunks)}\n")

for chunk in chunks:
    embedding = embedding_service.embed_text(chunk.text)

    print("=" * 60)
    print(f"Chunk ID : {chunk.chunk_id}")
    print(f"Embedding Dimension : {len(embedding)}")