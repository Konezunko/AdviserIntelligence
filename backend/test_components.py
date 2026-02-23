import os
import sys

# Add backend to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv()

print("--- Testing LLM ---")
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    print("LLM instantiated successfully.")
    # Try a simple invocation
    # resp = llm.invoke("Hello") 
    # print(f"LLM Response: {resp}")
except Exception as e:
    print(f"LLM Failed: {e}")
    import traceback
    traceback.print_exc()

print("\n--- Testing VectorStore ---")
try:
    from app.rag import get_vectorstore
    vs = get_vectorstore()
    if vs:
        print("VectorStore instantiated successfully.")
    else:
        print("VectorStore returned None.")
except Exception as e:
    print(f"VectorStore Failed: {e}")
    import traceback
    traceback.print_exc()
