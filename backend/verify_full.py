
import requests
import time

url = "http://127.0.0.1:8000/api/diagnose"
data = {"query": "紙が詰まった"}

print("--- Sending Request ---")
start = time.time()
try:
    response = requests.post(url, data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Elapsed: {time.time() - start:.2f}s")
    
    if response.status_code == 200:
        print("Response JSON:")
        print(response.json())
        print("SUCCESS: 200 OK received.")
    else:
        print(f"FAILURE: {response.text}")

except Exception as e:
    print(f"Request Error: {e}")
