"""
Application configuration using pydantic-settings.
Loads from environment variables with .env file support.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Configuration
    app_name: str = "NUVEXA Mobile API"
    app_version: str = "1.0.0"
    debug: bool = False

    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4"
    openai_max_tokens: int = 1000

    # CORS Configuration
    cors_origins: list[str] = [
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative dev port
        "https://*.vercel.app",   # Vercel deployments
        "https://*.netlify.app",  # Netlify deployments
    ]

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()
