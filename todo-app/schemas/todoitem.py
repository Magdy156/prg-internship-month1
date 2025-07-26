from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class TodoItemCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    due_date: Optional[datetime] = None
    priority: Optional[Priority] = None
    category: Optional[str] = None
    todolist_id: int

class TodoItemResponse(TodoItemCreate):
    id: int
    todolist_id: int
