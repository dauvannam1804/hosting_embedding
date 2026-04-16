# Embedding Service Professional

A production-ready Vector Embedding service built with FastAPI, Sentence-Transformers, and Docker. It features support for multiple models, API Key authentication, health monitoring, and seamless ngrok integration.

## New Features
- **Multi-Model Support**: Host multiple embedding models simultaneously.
- **RAM Optimization**: Implements **Lazy Loading** and **LRU Cache** to keep memory usage low (loads models only when requested and unloads older ones).
- **Security**: Secured via `X-API-KEY` header authentication.
- **Health Monitoring**: Detailed `/health` endpoint showing available models and service status.
- **Ngrok Integration**: Built-in support for public tunneling with Static Domains.

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/dauvannam1804/hosting_embedding.git
cd hosting_embedding
```

### 2. Configure Environment Variables
Copy the example environment file and update it with your credentials:
```bash
cp .env.example .env
```
Open `.env` and configure:
- `MODELS`: List of models in `alias:huggingface_id` format (e.g., `all-mpnet:sentence-transformers/all-mpnet-base-v2,harrier:microsoft/harrier-oss-v1-0.6b`).
- `DEFAULT_MODEL_ALIAS`: The model to use if none is specified in the request.
- `MAX_LOADED_MODELS`: Maximum number of models held in RAM at once (default is 1 for RAM efficiency).
- `API_KEY`: Your secret key for authentication.
- `NGROK_AUTHTOKEN` & `NGROK_DOMAIN`: For public access.

### 3. Deploy with Docker Compose
```bash
docker-compose up -d --build
```

---

## API Usage Examples

### 1. Generate Embeddings (Default Model)
```bash
curl -X POST "http://localhost:8000/embeddings" \
     -H "Content-Type: application/json" \
     -H "X-API-KEY: epidebate" \
     -d '{"input": ["Hello world"]}'
```

### 2. Generate Embeddings (Specific Model)
To use a specific model, provide the `model` alias defined in your `.env`.
```bash
curl -X POST "http://localhost:8000/embeddings" \
     -H "Content-Type: application/json" \
     -H "X-API-KEY: epidebate" \
     -d '{"input": ["Semantic search is powerful"], "model": "harrier"}'
```

### 3. Checking Service Health & Available Models
```bash
curl -H "X-API-KEY: epidebate" "http://localhost:8000/health"
```
**Response Example:**
```json
{
  "status": "ok",
  "available_models": {
    "all-mpnet": "sentence-transformers/all-mpnet-base-v2",
    "harrier": "microsoft/harrier-oss-v1-0.6b"
  },
  "default_model": "all-mpnet",
  "max_loaded_models": 1
}
```

## Project Structure
- `src/api`: API route definitions.
- `src/services`: Core logic for Lazy Loading and model orchestration.
- `src/core`: System configuration and security logic.
- `src/schemas`: Pydantic models for data validation.
- `run_app.py`: Automated startup script for local development.
- `test_multi_model.py`: Script to verify model switching and RAM limits.
