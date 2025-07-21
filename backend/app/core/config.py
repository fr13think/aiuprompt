from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Muat environment variables dari file .env
load_dotenv()

class Settings(BaseSettings):
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "default_key_if_not_set")

    class Config:
        case_sensitive = True

settings = Settings()