import time
import os
import sys

# Add backend to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv()

from app.rag import get_rag_diagnosis

print("--- Benchmarking Diagnosis ---")
start_time = time.time()

# First run (might trigger PDF loading)
print("1st Request (Cold Start)...")
result = get_rag_diagnosis("電源が入らない")
print(f"Time: {time.time() - start_time:.2f}s")

# Second run (Cached PDF)
print("\n2nd Request (Warm Cache)...")
start_time = time.time()
result = get_rag_diagnosis("電源が入らない")
print(f"Time: {time.time() - start_time:.2f}s")
