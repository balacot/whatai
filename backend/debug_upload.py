import requests

url = "http://localhost:8000/api/upload"
files = {'file': ('test.txt', 'This is a test document content for RAG.')}

try:
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")
