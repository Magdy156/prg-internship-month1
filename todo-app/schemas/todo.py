from pydantic import BaseModel
from datetime import datetime

class TodoBase(BaseModel):
    title: str

class TodoCreate(TodoBase):
    pass

class TodoResponse(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        from_attributes = True
