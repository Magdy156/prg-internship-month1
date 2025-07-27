from schemas.user import UserCreate, UserUpdate, UserResponse
from dal.repositories.user_repository import UserRepository
from utils.exceptions import UserNotFoundException
from utils.password_utils import get_password_hash

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create_user(self, user: UserCreate) -> UserResponse:
        hashed_password = get_password_hash(user.password)
        user_data = user.model_dump(exclude={"password"})
        user_data["password"] = hashed_password
        return self.user_repo.create_user(user_data)

    def get_user(self, user_id: int) -> UserResponse:
        return UserResponse.model_validate(self.user_repo.get_user_by_id(user_id))

    def get_user_by_username(self, username: str) -> UserResponse:
        return UserResponse.model_validate(self.user_repo.get_user_by_username(username))

    def update_user(self, user_id: int, user: UserUpdate) -> UserResponse:
        user_data = user.model_dump(exclude_unset=True)
        if "password" in user_data:
            user_data["password"] = get_password_hash(user_data["password"])
        return self.user_repo.update_user(user_id, user_data)

    def delete_user(self, user_id: int) -> dict:
        self.user_repo.delete_user(user_id)
        return {"detail": "User deleted"}
