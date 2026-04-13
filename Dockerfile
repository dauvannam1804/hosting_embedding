# Sử dụng Python image mỏng nhẹ
FROM python:3.11-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Cài đặt các thư viện hệ thống cần thiết (nếu có)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy file requirements và cài đặt python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn vào container
COPY src/ ./src/
COPY .env .

# Expose port ứng dụng
EXPOSE 8000

# Lệnh chạy ứng dụng
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
