from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from utils.exceptions import UserNotFoundException

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

    def create_user(self, user: UserCreate) -> User:
        db_user = User(**user.model_dump())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_user(self, user_id: int, user: UserCreate) -> User:
        db_user = self.get_user_by_id(user_id)
        update_data = user.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int):
        db_user = self.get_user_by_id(user_id)
        self.db.delete(db_user)
        self.db.commit()
