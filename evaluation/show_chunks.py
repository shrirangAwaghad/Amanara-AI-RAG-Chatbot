
import json
from pathlib import Path

chunks_file = Path("evaluation/chunks.json")

with chunks_file.open("r", encoding="utf-8") as file:
    chunks = json.load(file)

print(f"Total chunks: {len(chunks)}")

for chunk in chunks:
    text_preview = chunk.get("text", "")[:180].replace("\n", " ")

    print(f"\nChunk number: {chunk.get('chunk_id')}")
    print(f"Point ID: {chunk.get('point_id')}")
    print(f"Text: {text_preview}")
