
import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv

# Redirect stdout/stderr
sys.stdout = open("debug_standard.txt", "w", encoding="utf-8")
sys.stderr = sys.stdout

# Load env
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
api_key = os.environ.get("GOOGLE_API_KEY")

genai.configure(api_key=api_key)

print("--- Testing Standard Generation (gemini-1.5-flash) ---")
try:
    model = genai.GenerativeModel('models/gemini-flash-latest')
    response = model.generate_content("Hello, can you hear me?")
    print("SUCCESS")
    print(f"Response: {response.text[:50]}...")
except Exception as e:
    print(f"FAILED: {e}")
