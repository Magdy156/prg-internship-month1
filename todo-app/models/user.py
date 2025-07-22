from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from db.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, index=True, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
