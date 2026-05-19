from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User
from models.listing import Listing
from api.utils.auth import get_current_user
from core.database_config import get_db
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/purchase", tags=["purchase"])


@router.post("/buy/{listing_id}")
async def buy_artwork(
    listing_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.is_artist:
        raise HTTPException(
            status_code=400, detail="Художники не могут покупать работы"
        )

    result = await db.execute(
        select(Listing)
        .options(selectinload(Listing.artwork))
        .where(Listing.id == listing_id)
    )
    listing = result.scalar_one_or_none()

    if not listing:
        raise HTTPException(status_code=404, detail="Листинг не найден")

    if listing.is_sold:
        raise HTTPException(status_code=400, detail="Работа уже продана")

    price_float = float(listing.price)

    if current_user.balance < price_float:
        raise HTTPException(status_code=400, detail="Недостаточно средств на балансе")

    current_user.balance -= price_float
    listing.is_sold = True

    await db.commit()

    return {
        "message": "Покупка успешно завершена",
        "artwork_title": listing.artwork.title,
        "price": price_float,
        "new_balance": current_user.balance,
    }
