
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key present: {bool(api_key)}")
if api_key:
    # Print first few chars to verify it's the one we expect (AIza...)
    print(f"API Key starts with: {api_key[:4]}")

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Say hello")
    print("Gemini Test Success:")
    print(response.text)
except Exception as e:
    print("Gemini Test Failed:")
    print(e)
