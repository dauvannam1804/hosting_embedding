import subprocess
import time
import requests
import sys
import os

def run():
    print("--- Đang khởi động Embedding Service (Production Mode) ---")
    
    # 1. Khởi động uvicorn trong background
    print("[1/3] Khởi động FastAPI server trên port 8000...")
    uvicorn_cmd = ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
    # Nếu không dùng uv, hãy đổi thành: uvicorn_cmd = ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
    
    server_process = subprocess.Popen(
        uvicorn_cmd,
        stdout=subprocess.DEVNULL, # Chạy ngầm, không hiện log lênh terminal để tránh rối
        stderr=subprocess.STDOUT
    )

    # 2. Khởi động ngrok tunnel trong background
    print("[2/3] Khởi động ngrok tunnel...")
    ngrok_cmd = ["ngrok", "http", "8000"]
    ngrok_process = subprocess.Popen(
        ngrok_cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT
    )

    # Đợi một chút để ngrok thiết lập tunnel
    time.sleep(3)

    # 3. Lấy URL từ API của ngrok
    print("[3/3] Đang lấy Public URL...")
    public_url = None
    for i in range(10):
        try:
            response = requests.get("http://localhost:4040/api/tunnels")
            if response.status_code == 200:
                data = response.json()
                if data['tunnels']:
                    public_url = data['tunnels'][0]['public_url']
                    break
        except Exception:
            pass
        time.sleep(1)

    if public_url:
        print("\n" + "🟢" + "="*60)
        print(f"  Hệ thống đã sẵn sàng!")
        print(f"  🔗 URL Public:  {public_url}")
        print(f"  🔑 API Key:     epidebate")
        print(f"  🏥 Health:      {public_url}/health")
        print("  Sử dụng CTRL+C để dừng toàn bộ dịch vụ")
        print("="*60 + "\n")
    else:
        print("\n❌ Lỗi: Không lấy được URL từ ngrok. Hãy chắc chắn ngrok đã được cài đặt và cấu hình authtoken.")
        server_process.terminate()
        ngrok_process.terminate()
        sys.exit(1)

    try:
        # Giữ script chạy để duy trì tunnel và server
        while True:
            time.sleep(1)
            # Kiểm tra xem các process còn sống không
            if server_process.poll() is not None:
                print("⚠️ FastAPI server đã dừng đột ngột.")
                break
            if ngrok_process.poll() is not None:
                print("⚠️ Ngrok tunnel đã dừng đột ngột.")
                break
    except KeyboardInterrupt:
        print("\n--- Đang đóng các dịch vụ... ---")
    finally:
        server_process.terminate()
        ngrok_process.terminate()
        print("--- Đã dừng hệ thống. ---")

if __name__ == "__main__":
    run()
