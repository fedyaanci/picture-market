from sqlalchemy import Integer, ForeignKey, Boolean, Column, TIMESTAMP, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database_config import Base


class Listing(Base):
    __tablename__ = "listing"

    id = Column(Integer, primary_key=True, index=True)
    artwork_id = Column(Integer, ForeignKey("artwork.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    price = Column(Float, nullable=False)
    is_sold = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.now)
    sold_at = Column(TIMESTAMP, nullable=True)

    order = relationship("Order", backref="Listing", uselist=False)
