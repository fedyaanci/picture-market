from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from sqlalchemy.orm import selectinload

from api.schemas.artwork import ArtworkResponse
from api.schemas.artwork import ArtworkCreate
from models.artwork import Artwork
from models.user import User
from core.database_config import get_db
from api.utils.auth import get_current_user

router = APIRouter(prefix="/artworks", tags=["artworks"])


@router.get("/", response_model=List[ArtworkResponse])
async def get_artworks(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Artwork))
        artworks = result.scalars().all()
        return artworks
    except Exception as e:
        import traceback

        traceback.print_exc()
        return {"error": str(e), "code": "500"}


@router.get("/my", response_model=List[ArtworkResponse])
async def get_my_artworks(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    """Получает работы текущего пользователя"""
    if not current_user.is_artist:
        raise HTTPException(status_code=403, detail="User is not artist!")

    result = await db.execute(
        select(Artwork)
        .where(Artwork.artist_id == current_user.id)
        .options(selectinload(Artwork.listing))
    )
    artworks = result.scalars().all()
    return artworks


@router.get("/{artwork_id}", response_model=ArtworkResponse)
async def get_artwork(artwork_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Artwork).where(artwork_id == Artwork.id))
    form_result = result.scalar_one_or_none()
    if form_result is None:
        raise HTTPException(status_code=404, detail="artwork not found")
    return form_result


@router.post("/create", response_model=ArtworkResponse)
async def create_artwork(
    artwork: ArtworkCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not current_user.is_artist:
        raise HTTPException(status_code=403, detail="User is not artist!")

    new_artwork = Artwork(
        title=artwork.title,
        image_url=artwork.image_url,
        artist_id=current_user.id,
    )

    db.add(new_artwork)

    await db.commit()
    await db.refresh(new_artwork)

    return new_artwork
