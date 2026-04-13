from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    api_key: str = "epidebate"
    model_name: str = "sentence-transformers/all-mpnet-base-v2"
    host: str = "0.0.0.0"
    port: int = 8000
    ngrok_authtoken: str = ""
    ngrok_domain: str = ""
    
    # Cho phép đọc từ file .env và bỏ qua các trường thừa nếu có
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

settings = Settings()
