# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    DATABASE_URL: str
    ALGORITHM: str
    TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_SECRET_KEY: str
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    SYNC_DATABASE_URL: str

    class Config:
        env_file = ".env"   # For local development
        case_sensitive = True

settings = Settings()
