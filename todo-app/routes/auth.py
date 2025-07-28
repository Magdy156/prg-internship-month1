from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import UserCreateRequest, UserCreateResponse, UserReadResponse, UserLoginResponse
from schemas.token import TokenResponse
from services.auth_service import AuthService
from utils.dependencies import get_user_service
from services import UserService
from utils.auth_utils import get_current_user
from models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserCreateResponse)
def register_user(user: UserCreateRequest, user_service: UserService = Depends(get_user_service)):
    auth_service = AuthService(user_service)
    return auth_service.register_user(user)

@router.post("/login", response_model=UserLoginResponse)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), user_service: UserService = Depends(get_user_service)):
    auth_service = AuthService(user_service)
    return auth_service.login_user(form_data)

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str, user_service: UserService = Depends(get_user_service)):
    auth_service = AuthService(user_service)
    return await auth_service.refresh_user_token(refresh_token)

@router.post("/validate-token", response_model=UserReadResponse)
async def validate_token(current_user: User = Depends(get_current_user)):
    return UserReadResponse.model_validate(current_user)
