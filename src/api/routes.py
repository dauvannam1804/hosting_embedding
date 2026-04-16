from fastapi import APIRouter, Depends
from src.schemas.embedding import EmbeddingRequest, EmbeddingResponse
from src.services.embedding_service import embedding_service
from src.core.security import get_api_key
from src.core.config import settings

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "ok", 
        "available_models": settings.models_map,
        "default_model": settings.default_model_alias,
        "max_loaded_models": settings.max_loaded_models
    }

@router.post("/embeddings", response_model=EmbeddingResponse)
def get_embeddings(req: EmbeddingRequest, api_key: str = Depends(get_api_key)):
    embeddings = embedding_service.encode(req.input, req.model)
    return {
        "data": embeddings,
        "dim": len(embeddings[0]) if embeddings else 0
    }
