from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TodoListCreate(BaseModel):
    title: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class TodoListUpdate(TodoListCreate):
    pass

class TodoListResponse(TodoListCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True
        exclude = {"user"}
