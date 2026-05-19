from fastapi import APIRouter, HTTPException, Depends, status, security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from core.database_config import SessionLocal, get_db
from models.user import User
from api.schemas.user import UserResponse, UserLogin, UserBase, UserCreate

from api.utils.hash_pw import hash_password
from api.utils.verify import verify_password
from api.utils.auth import (
    create_access_token,
    verify_token_and_get_user,
    get_current_user,
)

router = APIRouter(prefix="/users", tags=["users"])

security = security.HTTPBearer()


@router.get("/me", response_model=UserResponse)
async def read_users_me(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
):
    token = credentials.credentials
    user = await verify_token_and_get_user(token, db)
    return user


@router.get("/", response_model=List[UserResponse])
async def get_users():
    try:
        async with SessionLocal() as session:
            stmt = select(User)
            result = await session.execute(stmt)

            users = result.scalars().all()

            print(f"Найдено {len(users)} пользователей")
            return users

    except Exception as e:
        print(f"Ошибка при получении пользователей: {e}")
        import traceback

        traceback.print_exc()
        return {"error": str(e), "code": "500"}


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    async with SessionLocal() as session:
        result = await session.execute(select(User).where(user_id == User.id))
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/register", response_model=UserBase)
async def register_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(data.username == User.username))

    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
        )

    hashed_pw = hash_password(data.password)

    new_user = User(
        username=data.username,
        password_hash=hashed_pw,
        is_artist=data.is_artist,
        avatar_url=data.avatar_url,
    )

    db.add(new_user)

    await db.commit()
    await db.refresh(new_user)

    return new_user


@router.post("/login")
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == data.username))

    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(user_id=user.id)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/balance/topup")
async def topup_balance(
    amount: float,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Сумма должна быть положительной")

    current_user.balance += amount
    await db.commit()
    return {"balance": current_user.balance}
