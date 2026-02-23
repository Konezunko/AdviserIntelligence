import sys
import os
import json

# Add backend to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv()

from app.rag import get_rag_diagnosis

query = "印刷に模様が出る"
print(f"--- Testing Query: {query} ---")

try:
    result = get_rag_diagnosis(query)
    print("\n--- Diagnosis Result ---")
    print(json.dumps(result, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Test Failed: {e}")
    import traceback
    traceback.print_exc()
