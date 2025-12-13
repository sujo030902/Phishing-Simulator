
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

with open("models_log.txt", "w") as f:
    f.write("--- Available Models ---\n")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                f.write(f"Name: {m.name} | Display: {m.display_name}\n")
    except Exception as e:
        f.write(f"Error: {e}\n")
    f.write("--- End ---\n")
print("Done writing models.")
