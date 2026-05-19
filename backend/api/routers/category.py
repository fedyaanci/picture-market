from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from api.schemas.category import CategoryResponse
from models.category import Category
from core.database_config import get_db

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=List[CategoryResponse])
async def get_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category))
    categories = result.scalars().all()
    return categories
