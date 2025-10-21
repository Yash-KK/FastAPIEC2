# app/config.py
from pydantic import conint
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    DATABASE_URL: str
    ALGORITHM: str
    TOKEN_EXPIRE_MINUTES: conint(gt=0) = 30
    REFRESH_SECRET_KEY: str
    REFRESH_TOKEN_EXPIRE_DAYS: conint(gt=0) = 7
    SYNC_DATABASE_URL: str

    class Config:
        env_file = ".env"   # local dev only
        case_sensitive = True

settings = Settings()
