from amanara.services.gemini_service import GeminiService


class IntentService:

    def __init__(self):
        self.gemini = GeminiService()

    def should_use_rag(self, question: str) -> bool:

        prompt = f"""
You are an intent classifier.

Classify the user's question into exactly ONE category.

GENERAL
- Renewable energy
- Solar energy
- Solar panels
- Net metering
- Government subsidies
- Sustainability
- Climate
- Energy storage
- Any general educational question

AMANARA
- Amanara
- Amanara Solar
- Amanara Solar Park
- Amanara services
- Amanara pricing
- Amanara consultation
- Amanara eligibility
- Amanara tariff
- Company-specific information
- Questions requiring Amanara documents

Return ONLY one word.

GENERAL

or

AMANARA

Question:
{question}
"""

        result = self.gemini.generate_response(prompt)

        return result.strip().upper() == "AMANARA"