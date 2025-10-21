from typing import Union

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_db
from app import models, schemas
from app.auth.dependencies import get_current_active_user
from app.auth.routers import router as auth_router

app = FastAPI()

app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"status": "Image built on EC2"}

@app.get("/only-auth")
def only_auth(
    db: AsyncSession = Depends(get_async_db),
    current_user: models.User = Depends(get_current_active_user)
):
    return {
        "status": "Yes you are authenticated"
    }

@app.get("/healthy")
def check_health():
    return {
        "status": "healthy"
    }
