import requests
import json

url = "http://localhost:8000/api/diagnose"
query = "コピー機背面の紙が詰まった"
payload = {"query": query}

print(f"Testing API with query: {query}")
try:
    response = requests.post(url, data=payload)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Response JSON:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    else:
        print("Error Response:")
        print(response.text)
except Exception as e:
    print(f"Request failed: {e}")
