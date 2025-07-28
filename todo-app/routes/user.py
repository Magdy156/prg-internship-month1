from fastapi import APIRouter, Depends, status
from schemas.user import UserUpdateRequest, UserReadResponse, UserUpdateResponse, UserDeleteResponse
from services.user_service import UserService
from models.user import User
from utils.auth_utils import get_current_user
from utils.dependencies import get_user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}", response_model=UserReadResponse)
def read_user(user_id: int, current_user: User = Depends(get_current_user), user_service: UserService = Depends(get_user_service)):
    return user_service.get_user(user_id)

@router.put("/{user_id}", response_model=UserUpdateResponse)
def update_user(user_id: int, user: UserUpdateRequest, current_user: User = Depends(get_current_user), user_service: UserService = Depends(get_user_service)):
    return user_service.update_user(user_id, user)

@router.delete("/{user_id}", response_model=UserDeleteResponse, status_code=status.HTTP_200_OK)
def delete_user(user_id: int, current_user: User = Depends(get_current_user), user_service: UserService = Depends(get_user_service)):
    return user_service.delete_user(user_id)
