import time
from google import genai

from amanara.config.settings import settings
from google.genai.errors import ServerError

class GeminiService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.google_api_key)

    def generate_response(self, prompt: str) -> str:
        delays = [2, 4, 8]

        for attempt, delay in enumerate(delays, start=1):
            try:
                print(f"Using model: {settings.llm_model}")

                response = self.client.models.generate_content(
                    model="gemini-flash-latest",
                    contents=prompt,
                )
                return response.text

            except ServerError as e:
                print(f"Attempt {attempt} failed: {e}")

                if attempt == len(delays):
                    raise RuntimeError(
                        "Gemini service is temporarily unavailable after multiple retry attempts."
                    ) from e

                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)