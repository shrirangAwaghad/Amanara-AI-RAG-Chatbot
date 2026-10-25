
from amanara.rag.loader import DocumentLoader
from amanara.rag.chunker import TextChunker

# Load the document; the cleaner now runs inside DocumentLoader.
loader = DocumentLoader()
documents = loader.load_documents()

# Generate chunks using the existing chunking configuration.
chunker = TextChunker()
chunks = chunker.chunk_documents(documents)

print(f"Documents loaded: {len(documents)}")
print(f"Total chunks generated: {len(chunks)}")

for chunk in chunks[:5]:
    print(f"\n--- Chunk {chunk.chunk_id} ---")
    print(f"Source: {chunk.source}")
    print(f"Characters: {len(chunk.text)}")
    print(chunk.text[:500])
