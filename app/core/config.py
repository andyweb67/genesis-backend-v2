# /core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    ANTHROPIC_API_KEY: str
    GENESIS_API_KEY: str  # ✅ ADD THIS LINE

    class Config:
        env_file = ".env"  # ✅ Points to your .env file for API keys

settings = Settings()

