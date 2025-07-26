from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime
from enum import Enum as PyEnum

class Priority(PyEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class TodoItem(Base):
    __tablename__ = "todoitems"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime)
    priority = Column(Enum(Priority, name="priority", create_type=True))
    category = Column(String)
    todolist_id = Column(Integer, ForeignKey("todolists.id"), nullable=False, index=True)

    todolist = relationship("TodoList")
