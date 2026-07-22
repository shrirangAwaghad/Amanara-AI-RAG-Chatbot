from amanara.rag.loader import DocumentLoader

loader = DocumentLoader()

documents = loader.load_documents()

print(f"Documents Loaded: {len(documents)}")

for i, doc in enumerate(documents, start=1):
    print("=" * 60)
    print(f"Document {i}")
    print(f"Source : {doc.source}")
    print(f"Characters : {len(doc.text)}")
    print(doc.text[:300])