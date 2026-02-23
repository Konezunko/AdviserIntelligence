
import os
import sys
from dotenv import load_dotenv

# Add current dir to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.rag import get_rag_diagnosis

# Load env
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

print("--- Testing get_rag_diagnosis directly ---")
try:
    result = get_rag_diagnosis("紙が詰まった")
    print("Diagnosis Result Keys:", result.keys())
    print("Probable Causes:", result.get("probable_causes"))
    if "error" in result or result.get("probable_causes") == ["Diagnosis failed (Fallback)"]:
        print("FAILURE: Fallback logic failed.")
        print(result)
    else:
        print("SUCCESS: Diagnosis generated.")
except Exception as e:
    print(f"EXCEPTION: {e}")
