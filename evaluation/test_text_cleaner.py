
from amanara.rag.loader import DocumentLoader
from amanara.rag.text_cleaner import clean_extracted_text

loader = DocumentLoader()
documents = loader.load_documents()

for document in documents:
    cleaned = clean_extracted_text(document.text)

    if "ElectricityAct" in document.text:
        start = document.text.find("TheElectricityAct")

        # Print a larger section to inspect the full paragraph.
        print("--- Original text ---")
        print(document.text[start:start + 1200])

        cleaned_start = cleaned.find("The Electricity Act")

        print("\n--- Cleaned text ---")
        print(cleaned[cleaned_start:cleaned_start + 1200])
        break
else:
    print("Electricity Act text not found.")
