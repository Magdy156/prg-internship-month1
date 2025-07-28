from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import UserCreateRequest, UserCreateResponse, UserReadResponse, UserLoginResponse
from schemas.token import TokenResponse
from services.user_service import UserService
from utils.auth_utils import create_access_token, create_refresh_token
from utils.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from utils.exceptions import InvalidCredentialsException, UsernameExistsException, UserNotFoundException, JWTDecodeException
from utils.password_utils import verify_password
from datetime import timedelta
from sqlalchemy.exc import IntegrityError
from jose import jwt, JWTError

class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def register_user(self, user: UserCreateRequest) -> UserCreateResponse:
        try:
            self.user_service.get_user_by_username(user.username)
            raise UsernameExistsException()
        except UserNotFoundException:
            try:
                return self.user_service.create_user(user)
            except IntegrityError as e:
                if "users_username_key" in str(e):
                    raise UsernameExistsException()
                raise

    def login_user(self, form_data: OAuth2PasswordRequestForm) -> UserLoginResponse:
        user = self.user_service.get_user_by_username_for_auth(form_data.username)
        if not user or not verify_password(form_data.password, user.password):
            raise InvalidCredentialsException()
        access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        refresh_token = create_refresh_token(data={"sub": user.username})
        return UserLoginResponse(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

    async def refresh_user_token(self, refresh_token: str) -> TokenResponse:
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise JWTDecodeException()
        except JWTError:
            raise JWTDecodeException()
        user = self.user_service.get_user_by_username(username)
        if user is None:
            raise UserNotFoundException()
        access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        return TokenResponse(access_token=access_token, token_type="bearer")
