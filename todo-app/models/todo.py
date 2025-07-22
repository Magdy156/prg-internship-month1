from sqlalchemy import Column, Integer, DateTime, String, Boolean, ForeignKey
from datetime import datetime, timezone
from db.database import Base

class Todo(Base):
    __tablename__  = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
