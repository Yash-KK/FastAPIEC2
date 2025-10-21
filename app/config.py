# app/config.py
from pydantic import conint
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Pydantic v2 configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"  # Ignore extra fields in .env
    )
    
    SECRET_KEY: str
    DATABASE_URL: str
    ALGORITHM: str
    TOKEN_EXPIRE_MINUTES: conint(gt=0) = 30
    REFRESH_SECRET_KEY: str
    REFRESH_TOKEN_EXPIRE_DAYS: conint(gt=0) = 7
    SYNC_DATABASE_URL: str

settings = Settings()