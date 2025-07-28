from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from schemas.token import TokenResponse

class UserCreateRequest(BaseModel):
    username: str
    email: str
    password: str

class UserCreateResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True
        exclude = {"todolists"}

class UserReadResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True
        exclude = {"todolists"}

class UserUpdateRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class UserUpdateResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True
        exclude = {"todolists"}

class UserDeleteResponse(BaseModel):
    detail: str

class UserLoginRequest(BaseModel):
    username: str
    password: str

class UserLoginResponse(TokenResponse):
    pass
