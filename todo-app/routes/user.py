from fastapi import APIRouter, Depends
from schemas.user import UserCreate, UserResponse
from services.user_service import UserService
from routes.auth import get_current_user
from models.user import User

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, user_service: UserService = Depends()):
    return user_service.create_user(user)

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, user_service: UserService = Depends(), current_user: User = Depends(get_current_user)):
    return user_service.get_user(user_id)

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate, user_service: UserService = Depends(), current_user: User = Depends(get_current_user)):
    return user_service.update_user(user_id, user)

@router.delete("/{user_id}")
def delete_user(user_id: int, user_service: UserService = Depends(), current_user: User = Depends(get_current_user)):
    return user_service.delete_user(user_id)
