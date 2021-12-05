from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP
from sqlalchemy.sql import func
from database import Base


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
