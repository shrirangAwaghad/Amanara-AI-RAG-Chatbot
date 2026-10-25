
from pathlib import Path
import fitz

pdf_path = Path("knowledge_base/Amanara_Company_Profile.pdf")

with fitz.open(pdf_path) as pdf:
    for page_number, page in enumerate(pdf, start=1):
        normal_text = page.get_text("text")
        block_text = page.get_text("blocks", sort=True)

        if "Electricity Act" in normal_text or "ElectricityAct" in normal_text:
            print(f"\nPAGE {page_number}")
            print("\n--- Normal extraction ---")
            print(normal_text[:4000])

            print("\n--- Block extraction ---")
            for block in block_text:
                if len(block) > 4 and isinstance(block[4], str):
                    print(block[4][:1000])

            break
    else:
        print("Target text was not found in the extracted PDF pages.")
