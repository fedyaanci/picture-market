from pydantic import BaseModel
from datetime import datetime


class OrderBase(BaseModel):
    listing_id: int
    buyer_id: int


class OrderCreate(BaseModel):
    listing_id: int


class OrderResponse(OrderBase):
    id: int
    purchased_at: datetime

    class Config:
        from_attributes = True
