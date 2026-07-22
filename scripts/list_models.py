from google import genai
from amanara.config.settings import settings

client = genai.Client(api_key=settings.google_api_key)

for model in client.models.list():
    print(f"{model.name}")
    print(f"  Supported: {model.supported_actions}")
    print()