import google.generativeai as genai
from core.config import get_google_api_keys

# Initial config with first key if available
api_keys = get_google_api_keys()
if api_keys:
    genai.configure(api_key=api_keys[0])

def generate_answer(prompt, temperature=0.3):
    # List of models to try in order (Fallback mechanism)
    models_to_try = [
        "gemini-2.5-flash-lite",
        "gemini-2.5-flash",
        "gemini-3-flash",
    ]

    # Refresh keys to ensure we have the latest list
    current_api_keys = get_google_api_keys()
    if not current_api_keys:
        raise ValueError("No Google API keys found. Please check secrets.toml.")

    last_error = None

    # 🔄 Outer Loop: Iterate through API Keys
    for key_index, api_key in enumerate(current_api_keys):
        try:
            # Configure with the current key
            genai.configure(api_key=api_key)
            
            # 🔄 Inner Loop: Iterate through Models
            for model_name in models_to_try:
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(
                        prompt,
                        generation_config={
                            "temperature": temperature,
                            "max_output_tokens": 1024
                        },
                        stream=True
                    )
                    return response
                except Exception as e:
                    print(f"⚠️ Key #{key_index+1} | Model {model_name} failed: {e}")
                    last_error = e
                    continue
            
            print(f"⚠️ All models failed for Key #{key_index+1}. Switching to next key...")
            
        except Exception as e:
            print(f"⚠️ Critical error with Key #{key_index+1}: {e}")
            last_error = e
            continue

    # If all models fail, raise the last error
    if last_error:
        raise last_error
