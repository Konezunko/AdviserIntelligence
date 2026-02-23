
import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv

# Redirect stdout and stderr to file
sys.stdout = open("debug_output_full.txt", "w", encoding="utf-8")
sys.stderr = sys.stdout

# Add current dir to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.rag import get_full_context, _ensure_cache, get_loaded_status

# Load env
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

print("--- Checking Manuals ---")
status = get_loaded_status()
print(f"Manuals found: {status['manuals']}")

print("\n--- Checking Full Context ---")
context = get_full_context()
print(f"Context Length: {len(context)} characters")

print("\n--- Attempting Cache Creation (using updated rag.py) ---")
try:
    cache = _ensure_cache()
    if cache:
        print(f"Cache created successfully: {cache.name}")
        print(f"Model used: {cache.model}")
        print(f"Expires: {cache.expire_time}")
    else:
        print("Cache creation returned None")
except Exception as e:
    print(f"Cache creation threw exception: {e}")
