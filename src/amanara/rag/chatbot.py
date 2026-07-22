from amanara.memory.conversation_memory import ConversationMemory
from amanara.rag.retriever import Retriever
from amanara.prompts.prompt_builder import PromptBuilder
from amanara.services.gemini_service import GeminiService


class AmanaraRAG:
    def __init__(self):
        
        self.retriever = Retriever()

        self.prompt_builder = PromptBuilder()

        self.gemini = GeminiService()
        
        self.memory = ConversationMemory()

    def ask(self, question: str, history: list):

        self.memory.add_user_message(question)

        chunks = self.retriever.retrieve(question)

        context = "\n\n".join(
            chunk.payload["text"]
            for chunk in chunks
        )

        history_text = "\n".join(
            f"{message['role'].capitalize()}: {message['content']}"
            for message in history
        )

        prompt = self.prompt_builder.build(
            query=question,
            context=context,
            history=history_text,
        )

        answer = self.gemini.generate_response(prompt)

        self.memory.add_assistant_message(answer)

        return {
            "answer": answer,
            "sources": chunks,
        }