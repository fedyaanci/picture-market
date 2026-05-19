import os
from core.database_config import get_db
from models.user import User
from datetime import datetime, timedelta

from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
""" 
Грубо говоря создаем движок распарса запросов 
    (ждем заголовок auth: bearer ....) / также схема безопасности 
"""
security = HTTPBearer()


""" 
Возвращает объект с: 
        scheme = "Bearer"
        credentials = "<токен>" 
"""


def create_access_token(user_id: int) -> str:
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {  # Данные которые будут закодированы в токен
        "user_id": user_id,
        "exp": expire,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)  # Подписывается payload


""" 
    acyncio.create_task(функция увед-я) чтобы пользовтаель не ждал
"""


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
):
    token = credentials.credentials  # Чистый jwtтокен

    credentials_exception = HTTPException(  # Ответ при невалидном токене
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception
    return user


async def verify_token_and_get_user(token: str, db: AsyncSession):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception
    return user


""" 
HTTPBearer отвечает за извлечение токена из HTTP-заголовка
verify_token_and_get_user отвечает за проверку токена и поиск пользователя
"""
