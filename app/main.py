from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "Worldddddd"}


@app.get("/healthy")
def check_health():
    return {
        "status": "healthy"
    }
