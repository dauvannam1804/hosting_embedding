from pydantic import BaseModel
from typing import List

class EmbeddingRequest(BaseModel):
    input: List[str]
    model: str = None  # Alias of the model to use

class EmbeddingResponse(BaseModel):
    data: List[List[float]]
    dim: int
