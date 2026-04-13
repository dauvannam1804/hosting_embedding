# Embedding Service Professional

A production-ready Vector Embedding service built with FastAPI, Sentence-Transformers, and Docker. It features API Key authentication, health monitoring, and seamless ngrok integration for easy public access.

## Features
- **High Performance**: Powered by `all-mpnet-base-v2` for high-quality semantic embeddings.
- **Security**: Secured via `X-API-KEY` header authentication.
- **Health Monitoring**: Dedicated `/health` endpoint for service status checks.
- **Fully Dockerized**: Build and deploy the entire stack with a single command.
- **Ngrok Integration**: Built-in support for public tunneling with Static Domains.

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Configure Environment Variables
Copy the example environment file and update it with your credentials:
```bash
cp .env.example .env
```
Open `.env` and configure:
- `API_KEY`: Your secret key for authentication.
- `NGROK_AUTHTOKEN`: Your token from the [ngrok dashboard](https://dashboard.ngrok.com).
- `NGROK_DOMAIN`: Your reserved free static domain from ngrok.

### 3. Deploy with Docker Compose
```bash
docker-compose up -d --build
```
The service will be available at `http://localhost:8000` and via your public ngrok URL.

---

## API Usage Examples

### Using cURL
```bash
curl -X POST "http://localhost:8000/embeddings" \
     -H "Content-Type: application/json" \
     -H "X-API-KEY: your-api-key" \
     -d '{"input": ["Hello world", "This is an example sentence"]}'
```

### Using Python (requests)
```python
import requests

url = "http://localhost:8000/embeddings"
headers = {
    "X-API-KEY": "your-api-key",
    "Content-Type": "application/json"
}
data = {
    "input": ["Hello world", "This is an example sentence"]
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

### Checking Service Health
```bash
curl -H "X-API-KEY: your-api-key" http://localhost:8000/health
```

## Project Structure
- `src/api`: API route definitions.
- `src/services`: Core logic for model loading and embedding generation.
- `src/core`: System configuration and security logic.
- `src/schemas`: Pydantic models for data validation.
- `Dockerfile` & `docker-compose.yml`: Containerization and orchestration setup.
- `run_app.py`: Automated startup script for local development.
