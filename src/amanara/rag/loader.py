import uuid
from amanara.models import document
from pathlib import Path

import fitz

from amanara.models.document import Document


class DocumentLoader:
    def __init__(self, knowledge_base: str = "knowledge_base"):
        self.knowledge_base = Path(knowledge_base)

    
    def load_documents(self) -> list[Document]:
        documents = []

        for file in self.knowledge_base.iterdir():

            if file.suffix.lower() == ".pdf":
                text = self._extract_pdf_text(file)

            elif file.suffix.lower() == ".txt":
                text = file.read_text(encoding="utf-8")

            else:
                continue
            
            document_id = str(uuid.uuid4())

            documents.append(
                Document(
                text=text,
                source=str(file),
                document_id=document_id
            )
        )

        return documents
    @staticmethod
    def _extract_pdf_text(pdf_path: Path) -> str:
        document = fitz.open(pdf_path)

        text = ""

        for page in document:
            text += page.get_text()

        document.close()

        return text