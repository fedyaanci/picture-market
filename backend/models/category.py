from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship
from core.database_config import Base


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    artworks = relationship(
        "Artwork", secondary="artwork_category", back_populates="categories"
    )
