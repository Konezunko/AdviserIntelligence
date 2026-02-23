import os
import sys

# Add backend to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from app.rag import get_vectorstore

print("--- Testing Chain Construction ---")
try:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    vs = get_vectorstore()
    retriever = vs.as_retriever(search_kwargs={"k": 3})
    
    print("Building RetrievalQA...")
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever
    )
    print("Chain built successfully.")
    
    print("Running Similarity Search...")
    docs = vs.similarity_search("test", k=1)
    print(f"Docs found: {len(docs)}")
    print(docs[0].page_content[:100])
    
    print("Running Chain...")
    # res = qa_chain.run("test")
    # print(res)
    
except Exception as e:
    print(f"Chain Failed: {e}")
    import traceback
    traceback.print_exc()
