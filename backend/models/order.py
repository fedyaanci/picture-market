from sqlalchemy import Integer, ForeignKey, Column, TIMESTAMP
from datetime import datetime
from core.database_config import Base


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listing.id"), unique=True, nullable=False)
    buyer_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    purchased_at = Column(TIMESTAMP, default=datetime.now)
