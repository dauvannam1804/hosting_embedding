import requests
import sys

# URL có thể truyền vào khi chạy script: python test_api.py https://xxxx.ngrok.io
URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
API_KEY = "epidebate"

print(f"Testing API at: {URL}")

# 1. Kiểm tra Health Check
try:
    health = requests.get(f"{URL}/health")
    print(f"Health Check: {health.json()}")
except Exception as e:
    print(f"Health Check failed: {e}")

# 2. Kiểm tra Embedding với Authentication
headers = {"X-API-KEY": API_KEY}
res = requests.post(
    f"{URL}/embeddings",
    json={"input": ["hello world"]},
    headers=headers
)

if res.status_code == 200:
    data = res.json()
    print("Success!")
    print(f"Keys: {data.keys()}")
    print(f"Dim: {data['dim']}")
    print(f"First 5 values: {data['data'][0][:5]}")
else:
    print(f"Error {res.status_code}: {res.text}")