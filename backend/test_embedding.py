import os
import sys

# Add backend to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import GoogleGenerativeAIEmbeddings

print("--- Testing text-embedding-004 ---")
try:
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    vec = embeddings.embed_query("hello world")
    print(f"Success! Vector length: {len(vec)}")
    print(vec[:5])
except Exception as e:
    print(f"Failed: {e}")
    import traceback
    traceback.print_exc()

print("\n--- Testing embedding-001 ---")
try:
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vec = embeddings.embed_query("hello world")
    print(f"Success! Vector length: {len(vec)}")
except Exception as e:
    print(f"Failed: {e}")
