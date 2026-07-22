from amanara.rag.loader import DocumentLoader
from amanara.rag.chunker import TextChunker

loader = DocumentLoader()
documents = loader.load_documents()

chunker = TextChunker(
    chunk_size=100,
    chunk_overlap=20,
)

chunks = chunker.chunk_documents(documents)

print(f"Total Chunks: {len(chunks)}\n")

for chunk in chunks:
    print("=" * 60)
    print(f"Chunk ID : {chunk.chunk_id}")
    print(f"Source   : {chunk.source}")
    print(f"Length   : {len(chunk.text)}")
    print(chunk.text)