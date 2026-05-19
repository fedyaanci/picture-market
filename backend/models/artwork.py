from sqlalchemy import Integer, String, Column, TIMESTAMP, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database_config import Base

artwork_category = Table(
    "artwork_category",
    Base.metadata,
    Column("artwork_id", Integer, ForeignKey("artwork.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("category.id"), primary_key=True),
)


class Artwork(Base):
    __tablename__ = "artwork"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    image_url = Column(String(500), nullable=False)
    artist_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now)

    rating = relationship("Rating", backref="artwork")
    listing = relationship("Listing", backref="artwork")
    artist = relationship("User", back_populates="artworks")
    categories = relationship(
        "Category", secondary=artwork_category, back_populates="artworks"
    )
