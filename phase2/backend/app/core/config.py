"""
Backend configuration using Pydantic Settings
Task: T-003 - Create Backend Environment Configuration
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    PROJECT_NAME: str = "Todo API"
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # Phase III: AI Configuration
    OPENAI_API_KEY: str = ""  # Get from https://platform.openai.com/api-keys
    OPENAI_AGENT_MODEL: str = "gpt-4o"  # GPT-4 Optimized
    GEMINI_API_KEY: str = ""  # Get from https://aistudio.google.com/app/apikey
    GEMINI_MODEL: str = "gemini-2.5-flash"  # Gemini model

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
