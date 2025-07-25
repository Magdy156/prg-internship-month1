from fastapi import Depends
from sqlalchemy.orm import Session
from dal.repositories.user_repository import UserRepository
from schemas.user import UserCreate, UserResponse
from db.database import get_db
from utils.auth_utils import get_password_hash

class UserService:
    def __init__(self, db: Session = Depends(get_db)):
        self.user_repo = UserRepository(db)

    def create_user(self, user: UserCreate) -> UserResponse:
        hashed_password = get_password_hash(user.password)
        user_data = UserCreate(
            username=user.username,
            email=user.email,
            password=hashed_password,
            created_at=user.created_at if hasattr(user, 'created_at') else None
        )
        return self.user_repo.create_user(user_data)

    def get_user(self, user_id: int) -> UserResponse:
        return self.user_repo.get_user_by_id(user_id)

    def get_user_by_username(self, username: str) -> UserResponse:
        return self.user_repo.get_user_by_username(username)

    def update_user(self, user_id: int, user: UserCreate) -> UserResponse:
        hashed_password = get_password_hash(user.password)
        user_data = UserCreate(
            username=user.username,
            email=user.email,
            password=hashed_password,
            created_at=user.created_at if hasattr(user, 'created_at') else None
        )
        return self.user_repo.update_user(user_id, user_data)

    def delete_user(self, user_id: int):
        self.user_repo.delete_user(user_id)
        return {"detail": "User deleted"}
