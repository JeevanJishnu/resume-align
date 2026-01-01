import requests
import json

url = "http://localhost:8000/v3/fill-template?template_name=Extractor_Master"

data = {
    "full_name": "Test User",
    "email": "test@test.com",
    "projects": [{"title": "P1"}]
}

try:
    print(f"POST {url}")
    res = requests.post(url, json=data)
    print(f"Status: {res.status_code}")
    print(f"Response: {res.text}")
except Exception as e:
    print(f"Exception: {e}")
