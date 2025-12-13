
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

try:
    genai.configure(api_key=api_key)
    # Try the newer model name
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Say hello")
    print("Gemini Test Success (gemini-1.5-flash):")
    print(response.text)
except Exception as e:
    print("Gemini Test Failed (gemini-1.5-flash):")
    print(e)
