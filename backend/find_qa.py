try:
    from langchain.chains import RetrievalQA
    print("Found in langchain.chains")
except ImportError as e:
    print(f"Not in langchain.chains: {e}")

try:
    from langchain_community.chains import RetrievalQA
    print("Found in langchain_community.chains")
except ImportError as e:
    print(f"Not in langchain_community.chains: {e}")
