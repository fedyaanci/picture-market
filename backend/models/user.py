from sqlalchemy import Integer, String, Boolean, Column, TIMESTAMP, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database_config import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_artist = Column(Boolean, default=False)
    avatar_url = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.now)
    balance = Column(Float, default=0.0)

    artworks = relationship("Artwork", back_populates="artist")
    ratings_given = relationship("Rating", backref="reviewer")
    orders = relationship("Order", backref="buyer")
    listings = relationship("Listing", backref="seller")
