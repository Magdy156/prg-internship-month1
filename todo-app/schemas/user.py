from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str
    password: str

class UserCreate(UserBase):
    pass

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
