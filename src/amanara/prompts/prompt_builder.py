class PromptBuilder:
    SYSTEM_PROMPT = """
You are Amanara AI, an intelligent assistant for Amanara Solar.

Answer ONLY using the provided context.

If the answer cannot be found in the context, reply:

"I don't have enough information to answer that."

Be concise, factual, and professional.
"""

    def build(
        self,
        query: str,
        context: str,
        history: str = "",
    ) -> str:

        prompt = f"""
{self.SYSTEM_PROMPT}

Conversation History:
-----------------------
{history}
-----------------------

Context:
-----------------------
{context}
-----------------------

Current Question:
{query}

Answer:
"""

        return prompt.strip()