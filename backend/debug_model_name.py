
import os
import sys
import google.generativeai as genai
from google.generativeai.caching import CachedContent
import datetime
from dotenv import load_dotenv

# Load env
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print("NO API KEY FOUND")
    exit(1)

genai.configure(api_key=api_key)

with open("debug_model.txt", "w", encoding="utf-8") as f:
    f.write(f"API Key found: {api_key[:5]}...\n")
    
    f.write("Listing models supporting caching:\n")
    try:
        found_flash = False
        for m in genai.list_models():
            if "createCachedContent" in m.supported_generation_methods:
                f.write(f"- {m.name}\n")
                if "gemini-1.5-flash" in m.name:
                    found_flash = True
        
        if not found_flash:
            f.write("WARNING: No gemini-1.5-flash model found with caching support.\n")

    except Exception as e:
        f.write(f"Error listing models: {e}\n")

    f.write("\nAttempting create with 'models/gemini-2.0-flash-001'...\n")
    try:
        cache = CachedContent.create(
            model='models/gemini-2.0-flash-001',
            display_name='test_cache_20',
            contents=['Hello'],
            ttl=datetime.timedelta(minutes=5)
        )
        f.write("SUCCESS: models/gemini-2.0-flash-001\n")
        cache.delete()
    except Exception as e:
        f.write(f"FAILED: models/gemini-2.0-flash-001: {e}\n")

    f.write("\nAttempting create with 'models/gemini-2.0-flash-lite-preview-09-2025'...\n")
    try:
        cache = CachedContent.create(
            model='models/gemini-2.0-flash-lite-preview-09-2025',
            display_name='test_cache_lite',
            contents=['Hello'],
            ttl=datetime.timedelta(minutes=5)
        )
        f.write("SUCCESS: models/gemini-2.0-flash-lite-preview-09-2025\n")
        cache.delete()
    except Exception as e:
        f.write(f"FAILED: models/gemini-2.0-flash-lite-preview-09-2025: {e}\n")
