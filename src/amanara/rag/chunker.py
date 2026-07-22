from amanara.models.document import Document
from amanara.models.chunk import Chunk


class TextChunker:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_documents(self, documents: list[Document]) -> list[Chunk]:
        chunks = []

        for document in documents:
            chunks.extend(self._chunk_document(document))

        return chunks

    def _chunk_document(self, document: Document) -> list[Chunk]:
        chunks = []

        text = document.text
        start = 0
        chunk_id = 1

        while start < len(text):
            end = start + self.chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    Chunk(
                        text=chunk_text,
                        source=document.source,
                        document_id=document.document_id,
                        chunk_id=chunk_id,
                    )
                )

            start += self.chunk_size - self.chunk_overlap
            chunk_id += 1

        return chunks