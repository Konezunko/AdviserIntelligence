import os
import sys

# Add backend to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv()

from app.rag import get_vectorstore, DB_DIR
print(f"DB_DIR: {DB_DIR}")

print("--- Debugging Retrieval ---")
query = "電源が入らない"
print(f"Query: {query}")

try:
    vs = get_vectorstore()
    if not vs:
        print("VectorStore is None.")
        sys.exit(1)
        
    # Search with higher k to see what's available
    docs = vs.similarity_search(query, k=5)
    
    print(f"\nFound {len(docs)} documents:\n")
    for i, doc in enumerate(docs):
        print(f"--- Doc {i+1} (Page {doc.metadata.get('page', '?')}) ---")
        print(doc.page_content.replace("\n", " ")[:200] + "...") # Print first 200 chars
        print("-" * 20)
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
