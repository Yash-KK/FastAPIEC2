from typing import Union

from fastapi import FastAPI
from app.database import get_async_db
from app import models, schemas
from app.auth.routers import router as auth_router

app = FastAPI()

app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"status": "Image built on EC2"}


@app.get("/healthy")
def check_health():
    return {
        "status": "healthy"
    }
