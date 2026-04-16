from sentence_transformers import SentenceTransformer
from src.core.config import settings
import logging
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        self._loaded_models = {}  # {alias: model_instance}
        self._load_order = []     # List to track LRU order
    
    def _get_model(self, model_alias: str):
        alias = model_alias or settings.default_model_alias
        
        # Check if alias exists in config
        if alias not in settings.models_map:
            raise HTTPException(status_code=400, detail=f"Model alias '{alias}' not found in configuration.")

        # Lazy loading
        if alias not in self._loaded_models:
            model_id = settings.models_map[alias]
            logger.info(f"Loading model: {alias} ({model_id})...")
            
            # Unload oldest model if limit reached
            if len(self._loaded_models) >= settings.max_loaded_models:
                oldest_alias = self._load_order.pop(0)
                logger.info(f"Unloading model to save RAM: {oldest_alias}")
                del self._loaded_models[oldest_alias]
            
            # Load new model
            try:
                # Harrier model might need dtype auto for optimization as identified in research
                model_kwargs = {"dtype": "auto"} if "harrier" in alias.lower() else {}
                self._loaded_models[alias] = SentenceTransformer(model_id, model_kwargs=model_kwargs)
                self._load_order.append(alias)
            except Exception as e:
                logger.error(f"Error loading model {alias}: {e}")
                raise HTTPException(status_code=500, detail=f"Failed to load model {alias}")
        else:
            # Update LRU order if already loaded
            if alias in self._load_order:
                self._load_order.remove(alias)
            self._load_order.append(alias)
            
        return self._loaded_models[alias]

    def encode(self, texts: list[str], model_alias: str = None):
        model = self._get_model(model_alias)
        embeddings = model.encode(texts).tolist()
        return embeddings

# Khởi tạo singleton instance
embedding_service = EmbeddingService()
