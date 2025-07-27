from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str
    password: str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    username: str | None = None  # Allow partial updates
    email: str | None = None
    password: str | None = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
        exclude = {"todolists"}  # Exclude the 'todolists' relationship
