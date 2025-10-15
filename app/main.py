from typing import Union

from fastapi import FastAPI
from app.database import get_db
from app import models, schemas
app = FastAPI()


@app.get("/")
def read_root():
    return {"statys": "Imaeg built on EC2"}


@app.get("/healthy")
def check_health():
    return {
        "status": "healthy"
    }
