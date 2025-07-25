from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TodoCreate(BaseModel):
    title: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class TodoResponse(TodoCreate):
    id: int
    user_id: int
