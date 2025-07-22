from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from models.todoitem import Priority

class TodoItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    due_date: Optional[datetime] = None
    priority: Priority = Priority.LOW
    category: Optional[str] = None
    todo_id: int

class TodoItemCreate(TodoItemBase):
    pass

class TodoItemResponse(TodoItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
