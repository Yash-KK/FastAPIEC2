import datetime

from app.database import get_async_db
from app.config import settings
from fastapi import APIRouter, Depends, HTTPException, status
from app.models import User
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.schemas import UserCreate, UserOut

from .schemas import Token, TokenRefresh
from .security import (create_access_token, create_refresh_token, get_pwd_hash,
                       verify_pwd, verify_refresh_token)

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(
    new_user: UserCreate,
    db: AsyncSession = Depends(get_async_db)
):
    stmt = select(User).where(User.email == new_user.email)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    hashed_password = get_pwd_hash(new_user.password)
    db_user = User(
        email=new_user.email,
        hashed_password=hashed_password,
        username=new_user.username,
        full_name=new_user.full_name,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_db)
):
    stmt = select(User).where(User.email == form_data.username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user or not verify_pwd(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    access_token_expires = datetime.timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = datetime.timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user.email},
        expires_delta=refresh_token_expires
    )
    
    return {
        "access_token": token, 
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(
    token_data: TokenRefresh,
    db: AsyncSession = Depends(get_async_db)
):
    email = verify_refresh_token(token_data.refresh_token)
    
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    access_token_expires = datetime.timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "refresh_token": token_data.refresh_token,
        "token_type": "bearer"
    }