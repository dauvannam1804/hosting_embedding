from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    api_key: str = "epidebate"
    models: str = "all-mpnet:sentence-transformers/all-mpnet-base-v2,harrier:microsoft/harrier-oss-v1-0.6b"
    default_model_alias: str = "all-mpnet"
    max_loaded_models: int = 1
    host: str = "0.0.0.0"
    port: int = 8000
    ngrok_authtoken: str = ""
    ngrok_domain: str = ""
    
    @property
    def models_map(self) -> dict[str, str]:
        """Parses the MODELS string into a dictionary {alias: id}."""
        try:
            return dict(item.split(":") for item in self.models.split(",") if ":" in item)
        except Exception:
            return {"all-mpnet": "sentence-transformers/all-mpnet-base-v2"}

    # Cho phép đọc từ file .env và bỏ qua các trường thừa nếu có
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

settings = Settings()
