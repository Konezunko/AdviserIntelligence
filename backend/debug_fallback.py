
import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv

# Redirect stdout/stderr
sys.stdout = open("debug_fallback.txt", "w", encoding="utf-8")
sys.stderr = sys.stdout

# Load env
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
api_key = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

print("--- Testing Generation Fallback ---")
dummy_context = "x" * 30000 # 30k chars

models_to_try = [
    'models/gemini-flash-latest',
    'models/gemini-pro-latest',
    'models/gemini-2.5-flash',
    'models/gemini-2.0-flash-lite',
    'gemini-1.5-flash'
]

for m_name in models_to_try:
    print(f"\nTesting model: {m_name}")
    try:
        model = genai.GenerativeModel(m_name)
        response = model.generate_content(f"Hi, this is a test. Context: {dummy_context[:100]}...")
        print("SUCCESS")
        print(f"Response: {response.text[:50]}...")
    except Exception as e:
        print(f"FAILED: {e}")
