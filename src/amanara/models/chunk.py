from dataclasses import dataclass


@dataclass
class Chunk:
    text: str
    source: str
    document_id: str
    chunk_id: int