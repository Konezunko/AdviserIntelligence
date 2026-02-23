import sys
import os

# Ensure backend dir is in path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

try:
    from app.rag import get_rag_diagnosis
    print("Import successful. Running diagnosis...")
    result = get_rag_diagnosis("コピー機背面の紙が詰まった")
    print("Diagnosis Result:")
    print(result)
except Exception as e:
    import traceback
    traceback.print_exc()
