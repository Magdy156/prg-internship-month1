from fastapi import Depends
from sqlalchemy.orm import Session
from services.auth_service import AuthService
from services.user_service import UserService
from dal.repositories.user_repository import UserRepository
from db.database import get_db

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    return AuthService(user_service)
