import os
import sys

# Add backend to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv()

from app.rag import ingest_manuals, get_vectorstore

print("--- Re-Ingesting Manuals ---")
try:
    res = ingest_manuals()
    print(res)
    
    # Verify file creation
    import os
    from app.rag import DB_DIR
    print(f"Checking DB_DIR: {DB_DIR}")
    print(f"Files: {os.listdir(DB_DIR)}")
except Exception as e:
    print(f"Ingestion Failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n--- Testing Similarity Search ---")
try:
    vs = get_vectorstore()
    if not vs:
        print("VectorStore is None after ingestion!")
        sys.exit(1)
        
    print("Searching for '電源が入らない'...")
    docs = vs.similarity_search("電源が入らない", k=3)
    print(f"Docs found: {len(docs)}")
    if docs:
        print(f"Content: {docs[0].page_content[:50]}...")
        print(f"Metadata: {docs[0].metadata}")
except Exception as e:
    print(f"Search Failed: {e}")
    import traceback
    traceback.print_exc()
