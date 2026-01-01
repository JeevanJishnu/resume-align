
import requests
import os

API_BASE_URL = "http://localhost:8000"
CV_PATH = "input/20251223_104401_AM0209_Vineetha Thamban .pdf"
TEMPLATE_NAME = "AM0275 Vishnuraj K J" # One of the registered ones

def test_conversion():
    if not os.path.exists(CV_PATH):
        print(f"CV not found at {CV_PATH}")
        return

    with open(CV_PATH, 'rb') as f:
        files = {"file": (os.path.basename(CV_PATH), f, "application/pdf")}
        url = f"{API_BASE_URL}/process-to-template?template_name={TEMPLATE_NAME}"
        print(f"Sending request to {url}...")
        try:
            res = requests.post(url, files=files)
            print(f"Status Code: {res.status_code}")
            if res.status_code != 200:
                print(f"Error Response: {res.text}")
            else:
                print("Success! Response size:", len(res.content))
        except Exception as e:
            print(f"Request failed: {e}")

if __name__ == "__main__":
    # Ensure server is running: this script assumes it is.
    test_conversion()
