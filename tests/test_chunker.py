import pytest

from amanara.models.document import Document
from amanara.rag.chunker import TextChunker


def make_document(text: str) -> Document:
    return Document(
        text=text,
        source="test_document.pdf",
        document_id="test-document",
    )


def test_rejects_nonpositive_chunk_size():
    with pytest.raises(ValueError, match="chunk_size must be positive"):
        TextChunker(chunk_size=0)


def test_rejects_negative_overlap():
    with pytest.raises(ValueError, match="chunk_overlap"):
        TextChunker(chunk_size=10, chunk_overlap=-1)


def test_rejects_overlap_equal_to_chunk_size():
    with pytest.raises(ValueError, match="chunk_overlap"):
        TextChunker(chunk_size=10, chunk_overlap=10)


def test_empty_document_produces_no_chunks():
    chunker = TextChunker(chunk_size=10, chunk_overlap=2)

    assert chunker.chunk_documents([make_document("   ")]) == []


def test_short_document_produces_one_chunk():
    chunker = TextChunker(chunk_size=100, chunk_overlap=10)
    document = make_document("Solar energy is renewable.")

    chunks = chunker.chunk_documents([document])

    assert len(chunks) == 1
    assert chunks[0].text == "Solar energy is renewable."


def test_chunks_preserve_document_metadata():
    chunker = TextChunker(chunk_size=20, chunk_overlap=5)
    document = make_document(
        "Solar energy supports clean electricity generation."
    )

    chunks = chunker.chunk_documents([document])

    assert len(chunks) > 0

    for chunk in chunks:
        assert chunk.source == document.source
        assert chunk.document_id == document.document_id


def test_chunk_ids_start_at_one_and_increase():
    chunker = TextChunker(chunk_size=20, chunk_overlap=5)
    document = make_document(
        "Solar energy supports clean electricity generation."
    )

    chunks = chunker.chunk_documents([document])

    assert [chunk.chunk_id for chunk in chunks] == list(
        range(1, len(chunks) + 1)
    )
