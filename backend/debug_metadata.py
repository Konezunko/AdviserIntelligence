import os
import sys

# Add backend to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv()

from app.rag import get_vectorstore

print("--- Inspecting Vector Store Metadata ---")
try:
    vs = get_vectorstore()
    if not vs:
        print("VectorStore is None.")
        sys.exit(1)
        
    print("Searching for 'test' to inspect metadata...")
    docs = vs.similarity_search("test", k=1)
    if docs:
        print(f"Metadata found: {docs[0].metadata}")
    else:
        print("No documents found.")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
