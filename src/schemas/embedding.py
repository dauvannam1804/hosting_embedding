from pydantic import BaseModel
from typing import List

class EmbeddingRequest(BaseModel):
    input: List[str]

class EmbeddingResponse(BaseModel):
    data: List[List[float]]
    dim: int
