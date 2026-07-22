from amanara.services.gemini_service import GeminiService

service = GeminiService()

while True:
    prompt = input("\nYou: ")

    if prompt.lower() in ["exit", "quit"]:
        break

    response = service.generate_response(prompt)

    print(f"\nGemini: {response}")