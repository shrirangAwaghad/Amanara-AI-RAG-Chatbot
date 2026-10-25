from amanara.rag.text_cleaner import clean_extracted_text
import uuid
from pathlib import Path

import fitz

from amanara.models.document import Document


class DocumentLoader:
    def __init__(self, knowledge_base: str = "knowledge_base"):
        self.knowledge_base = Path(knowledge_base)

    def load_documents(self) -> list[Document]:
        documents = []

        if not self.knowledge_base.exists():
            raise FileNotFoundError(
                f"Knowledge base folder not found: {self.knowledge_base}"
            )

        for file in sorted(self.knowledge_base.iterdir()):
            if file.suffix.lower() == ".pdf":
                text = self._extract_pdf_text(file)
            elif file.suffix.lower() == ".txt":
                text = file.read_text(encoding="utf-8")
            else:
                continue

             # Clean extracted text before validation and chunking.
            text = clean_extracted_text(text)
            
            if not text.strip():
                print(f"Warning: No text extracted from {file.name}")
                continue

            documents.append(
                Document(
                    text=text,
                    source=str(file),
                    document_id=str(uuid.uuid4()),
                )
            )

        return documents

    @staticmethod
    def _extract_pdf_text(pdf_path: Path) -> str:
        page_texts = []

        with fitz.open(pdf_path) as pdf:
            for page in pdf:
                page_text = page.get_text("text")
                page_texts.append(page_text.strip())

        return "\n\n".join(
            text for text in page_texts if text
        )
