from sqlalchemy import (
    Integer,
    ForeignKey,
    Column,
    SmallInteger,
    TIMESTAMP,
    CheckConstraint,
)
from datetime import datetime
from core.database_config import Base


class Rating(Base):
    __tablename__ = "rating"

    id = Column(Integer, primary_key=True, index=True)
    artwork_id = Column(Integer, ForeignKey("artwork.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    score = Column(SmallInteger, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now)

    __table_args__ = (
        CheckConstraint("score >= 1 AND score <= 5", name="check_score_range"),
    )
