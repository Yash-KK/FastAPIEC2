import enum
import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    password: str
