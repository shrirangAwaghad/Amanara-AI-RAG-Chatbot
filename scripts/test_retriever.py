from amanara.rag.retriever import Retriever

retriever = Retriever()

query = "What services does Amanara provide?"

results = retriever.retrieve(query)

print(f"Results Found: {len(results)}\n")

for i, result in enumerate(results, start=1):
    print(result.payload)
    print("-" * 80)