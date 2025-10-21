from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
ALGORITHM = os.getenv("ALGORITHM")
TOKEN_EXPIRE_MINUTES = os.getenv("TOKEN_EXPIRE_MINUTES")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
REFRESH_TOKEN_EXPIRE_DAYS = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")
SYNC_DATABASE_URL = os.getenv("SYNC_DATABASE_URL")
class Settings(BaseSettings):
    DATABASE_URL: str = DATABASE_URL
    SECRET_KEY: str = SECRET_KEY
    ALGORITHM: str = ALGORITHM
    TOKEN_EXPIRE_MINUTES: int = 30 
    REFRESH_SECRET_KEY: str = REFRESH_SECRET_KEY
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(REFRESH_TOKEN_EXPIRE_DAYS)
    SYNC_DATABASE_URL: str = SYNC_DATABASE_URL
    class Config:
        env_file = ".env"


settings = Settings()
