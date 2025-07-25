from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from fastapi import HTTPException, status

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> User:
        user = self.db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    def get_user_by_username(self, username: str) -> User:
        user = self.db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    def create_user(self, user: UserCreate) -> User:
        db_user = User(
            username=user.username,
            email=user.email,
            password=user.password,
            created_at=user.created_at if hasattr(user, 'created_at') else None
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_user(self, user_id: int, user: UserCreate) -> User:
        db_user = self.get_user_by_id(user_id)
        db_user.username = user.username
        db_user.email = user.email
        db_user.password = user.password
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int):
        db_user = self.get_user_by_id(user_id)
        self.db.delete(db_user)
        self.db.commit()
