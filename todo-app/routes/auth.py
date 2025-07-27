from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import UserCreate, UserResponse
from schemas.token import TokenResponse
from services.auth_service import AuthService
from utils.dependencies import get_user_service
from services import UserService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, user_service: UserService = Depends(get_user_service)):
    auth_service = AuthService(user_service)
    return auth_service.register_user(user)

@router.post("/login", response_model=TokenResponse)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), user_service: UserService = Depends(get_user_service)):
    auth_service = AuthService(user_service)
    return auth_service.login_user(form_data)

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str, user_service: UserService = Depends(get_user_service)):
    auth_service = AuthService(user_service)
    return await auth_service.refresh_user_token(refresh_token)
