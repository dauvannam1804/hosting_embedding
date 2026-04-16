import requests
import time

URL = "http://localhost:8000"
API_KEY = "epidebate"
headers = {"X-API-KEY": API_KEY}

def test_model(alias, input_text):
    print(f"\n--- Testing model: {alias} ---")
    start = time.time()
    res = requests.post(
        f"{URL}/embeddings",
        json={"input": [input_text], "model": alias},
        headers=headers
    )
    duration = time.time() - start
    if res.status_code == 200:
        data = res.json()
        print(f"Success! Time: {duration:.2f}s")
        print(f"Dim: {data['dim']}")
        print(f"First 3 values: {data['data'][0][:3]}")
    else:
        print(f"Error {res.status_code}: {res.text}")

if __name__ == "__main__":
    # 1. Health check to see config
    print("Checking health...")
    print(requests.get(f"{URL}/health").json())

    # 2. Test default model (all-mpnet)
    test_model(None, "Hello from default")

    # 3. Test harrier model (should trigger loading and unload default)
    test_model("harrier", "Hello from harrier")

    # 4. Test default again (should trigger reload since limit is 1)
    test_model("all-mpnet", "Back to default")
