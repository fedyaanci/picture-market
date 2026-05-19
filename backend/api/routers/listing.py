from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from api.schemas.listing import ListingResponse, ListingCreate
from models.artwork import Artwork
from models.listing import Listing

from api.utils.auth import get_current_user
from models.user import User
from core.database_config import get_db
from fastapi import Query

router = APIRouter(prefix="/listing", tags=["listing"])


@router.get("/", response_model=List[ListingResponse])
async def get_listings(is_sold: bool = Query(None), db: AsyncSession = Depends(get_db)):
    query = select(Listing)

    if is_sold is not None:
        query = query.where(Listing.is_sold == is_sold)

    result = await db.execute(query)

    return result.scalars().all()


@router.post("/", response_model=ListingResponse)
async def create_listing(
    listing_data: ListingCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not current_user.is_artist:
        raise HTTPException(status_code=403, detail="Only artists can create listings")

    artwork = await db.get(Artwork, listing_data.artwork_id)  # сущ-е арта

    if not artwork:
        raise HTTPException(status_code=404, detail="Artwork not found")

    if artwork.artist_id != current_user.id:  # принадлежность арта
        raise HTTPException(status_code=403, detail="You don't own this artwork")

    existing_listing = await db.execute(  # нету ли листинга для арта
        select(Listing).where(Listing.artwork_id == listing_data.artwork_id)
    )
    if existing_listing.scalar_one_or_none():
        raise HTTPException(
            status_code=400, detail="Listing already exists for this artwork"
        )

    new_listing = Listing(
        artwork_id=listing_data.artwork_id,
        seller_id=current_user.id,
        price=listing_data.price,
        is_sold=False,
    )
    db.add(new_listing)
    await db.commit()
    await db.refresh(new_listing)

    return new_listing
