
import re

from amanara.models.document import Document
from amanara.models.chunk import Chunk


class TextChunker:
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
    ):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")

        if chunk_overlap < 0 or chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be >= 0 and < chunk_size"
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_documents(
        self, documents: list[Document]
    ) -> list[Chunk]:
        chunks = []

        for document in documents:
            chunks.extend(self._chunk_document(document))

        return chunks

    def _chunk_document(
        self, document: Document
    ) -> list[Chunk]:
        text = re.sub(r"\s+", " ", document.text).strip()

        if not text:
            return []

        chunks = []
        start = 0
        chunk_id = 1
        text_length = len(text)

        while start < text_length:
            end = min(start + self.chunk_size, text_length)

            # Prefer a sentence boundary near the target end.
            if end < text_length:
                boundary = text.rfind(". ", start, end)

                # Use the boundary only if it is reasonably close
                # to the target end; otherwise keep the hard limit.
                if boundary >= start + self.chunk_size // 2:
                    end = boundary + 1

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
                chunk_id += 1

            if end >= text_length:
                break

            # Continue with overlap while ensuring forward progress.
            next_start = max(start + 1, end - self.chunk_overlap)

            # Avoid starting the next chunk in the middle of a word.
            space_position = text.find(" ", next_start, end)
            if space_position != -1:
                next_start = space_position + 1

            start = next_start

        return chunks
