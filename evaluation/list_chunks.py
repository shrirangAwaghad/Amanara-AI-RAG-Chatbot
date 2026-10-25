
import json
from pathlib import Path

from amanara.config.settings import settings
from amanara.services.qdrant_service import QdrantService


def main():
    service = QdrantService()

    points, _ = service.client.scroll(
        collection_name=settings.qdrant_collection,
        limit=100,
        with_payload=True,
        with_vectors=False,
    )

    output = []

    for point in points:
        payload = point.payload or {}

        output.append({
            "point_id": str(point.id),
            "chunk_id": payload.get("chunk_id"),
            "source": payload.get("source", "Unknown"),
            "text": payload.get("text", ""),
        })

    output_path = Path("evaluation/chunks.json")
    output_path.write_text(
        json.dumps(output, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"Total chunks exported: {len(output)}")
    print(f"Saved to: {output_path.resolve()}")


if __name__ == "__main__":
    main()
