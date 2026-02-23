import sys
import os

try:
    import langchain
    print(f"langchain version: {getattr(langchain, '__version__', 'unknown')}")
    print(f"langchain file: {langchain.__file__}")
    print(f"langchain path: {langchain.__path__}")
except ImportError as e:
    print(f"Error importing langchain: {e}")

try:
    import langchain.chains
    print(f"langchain.chains file: {langchain.chains.__file__}")
except ImportError as e:
    print(f"Error importing langchain.chains: {e}")

try:
    from langchain.chains import RetrievalQA
    print("RetrievalQA imported successfully")
except ImportError as e:
    print(f"Error importing RetrievalQA: {e}")

# Check pip list from within python
try:
    import pkg_resources
    dists = [d for d in pkg_resources.working_set]
    for d in dists:
        if 'langchain' in d.project_name:
            print(f"{d.project_name} {d.version}")
except Exception as e:
    print(f"Error checking packages: {e}")
