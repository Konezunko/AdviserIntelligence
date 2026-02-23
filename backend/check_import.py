try:
    import langchain
    print(f"langchain: {langchain.__version__}")
    print(f"file: {langchain.__file__}")
    from langchain.chains import RetrievalQA
    print("Import successful")
except ImportError as e:
    print(f"Error: {e}")
    try:
        import langchain.chains
        print("langchain.chains imported")
    except ImportError as e2:
        print(f"Error importing chains: {e2}")
except Exception as e:
    print(f"Other Error: {e}")
