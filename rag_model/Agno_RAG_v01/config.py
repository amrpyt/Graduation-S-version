from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    # Supabase settings
    supabase_url: str
    supabase_key: str
    supabase_jwt_secret: str

    # JWT settings
    jwt_secret_key: str
    token_expire_minutes: int = 60 * 24  # 24 hours

    # Google AI settings
    google_api_key: str

    # Gemini Model settings
    gemini_model: str = "gemini-2.0-flash"
    gemini_temperature: float = 0.7
    gemini_top_p: float = 0.95
    gemini_top_k: int = 40
    gemini_max_output_tokens: int = 2048
    gemini_embedding_model: str = "models/text-embedding-004"

    # Database settings
    db_collection: str = "documents"
    embeddings_collection: str = "embeddings"

    # Application settings
    environment: str = "development"
    debug: bool = True
    app_name: str = "Agno RAG"

    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    return Settings() 