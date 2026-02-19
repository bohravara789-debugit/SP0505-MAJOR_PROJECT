import google.generativeai as genai
from core.config import get_google_api_key

genai.configure(api_key=get_google_api_key())

def generate_answer(prompt, temperature=0.3):
    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": temperature,
            "max_output_tokens": 1024
        },
        stream=True
    )

    return response
