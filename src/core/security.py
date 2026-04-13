from fastapi import HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from src.core.config import settings

API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(header_api_key: str = Depends(api_key_header)):
    if header_api_key == settings.api_key:
        return header_api_key
    raise HTTPException(status_code=403, detail="Could not validate API Key")
