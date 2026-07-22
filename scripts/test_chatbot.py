from amanara.rag.chatbot import AmanaraRAG

chatbot = AmanaraRAG()

question = "What services does Amanara provide?"

answer = chatbot.ask(question)

print("\nQuestion:")
print(question)

print("\nAnswer:")
print(answer)