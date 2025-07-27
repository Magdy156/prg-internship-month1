from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserResponse
from utils.exceptions import UserNotFoundException
from datetime import datetime, timezone

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> User:
        user = self.db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise UserNotFoundException()
        return user

    def get_user_by_username(self, username: str) -> User:
        user = self.db.query(User).filter(User.username == username).first()
        if user is None:
            raise UserNotFoundException()
        return user

    def create_user(self, user_data: dict) -> UserResponse:
        db_user = User(**user_data, created_at=datetime.now(timezone.utc))
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return UserResponse.model_validate(db_user)

    def update_user(self, user_id: int, user_data: dict) -> UserResponse:
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if db_user is None:
            raise UserNotFoundException()
        self.db.query(User).filter(User.id == user_id).update(user_data)
        self.db.commit()
        self.db.refresh(db_user)
        return UserResponse.model_validate(db_user)

    def delete_user(self, user_id: int):
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if db_user is None:
            raise UserNotFoundException()
        self.db.delete(db_user)
        self.db.commit()
