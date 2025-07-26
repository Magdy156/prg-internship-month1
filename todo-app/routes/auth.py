from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from models.user import User
from db.database import get_db
from services.user_service import UserService
from utils.auth_utils import verify_password
from utils.exceptions import InvalidCredentialsException, JWTDecodeException
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/auth", tags=["auth"])

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "Default")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_access_token(data: dict, expires_delta: timedelta = None):
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        print(f"Creating token with payload: {to_encode}")
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        print(f"Token created: {encoded_jwt[:10]}...")
        return encoded_jwt
    except Exception as e:
        print(f"JWT encoding error: {str(e)}")
        raise

async def get_current_user(token: str = Depends(oauth2_scheme), user_service: UserService = Depends()):
    try:
        print(f"Decoding token: {token[:10]}...")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Token payload: {payload}")
        username: str = payload.get("sub")
        if username is None:
            print("No username in token payload")
            raise JWTDecodeException()
        user = user_service.get_user_by_username(username)
        print(f"User found: {user.username}")
        return user
    except JWTError:
        print("JWT decode error")
        raise JWTDecodeException()

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), user_service: UserService = Depends()):
    try:
        print(f"Login attempt for username: {form_data.username}")
        user = user_service.get_user_by_username(form_data.username)
        print(f"User query result: {user.username}")
        if not verify_password(form_data.password, user.password):
            print("Login failed: Incorrect password")
            raise InvalidCredentialsException()
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        print(f"Login successful, token: {access_token[:10]}...")
        return {"access_token": access_token, "token_type": "bearer"}
    except InvalidCredentialsException:
        raise
    except Exception as e:
        print(f"Unexpected login error: {str(e)}")
        raise
