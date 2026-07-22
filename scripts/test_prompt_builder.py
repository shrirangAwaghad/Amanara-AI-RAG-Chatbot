from amanara.rag.retriever import Retriever
from amanara.prompts.prompt_builder import PromptBuilder

retriever = Retriever()
builder = PromptBuilder()

query = "What services does Amanara provide?"

chunks = retriever.retrieve(query)

prompt = builder.build(query, chunks)

print(prompt)