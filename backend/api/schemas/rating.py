from pydantic import BaseModel
from datetime import datetime


class RatingBase(BaseModel):
    artist_id: int
    reviewer_id: int
    score: int


class RatingCreate(RatingBase):
    pass


class RatingResponse(RatingBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
