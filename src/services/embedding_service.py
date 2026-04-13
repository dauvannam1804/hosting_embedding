from sentence_transformers import SentenceTransformer
from src.core.config import settings

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer(settings.model_name)
    
    def encode(self, texts: list[str]):
        embeddings = self.model.encode(texts).tolist()
        return embeddings

# Khởi tạo singleton instance
embedding_service = EmbeddingService()
