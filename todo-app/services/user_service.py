from schemas.user import UserCreateRequest, UserCreateResponse, UserReadResponse, UserUpdateRequest, UserUpdateResponse, UserDeleteResponse
from dal.repositories.user_repository import UserRepository
from utils.exceptions import UserNotFoundException
from utils.password_utils import get_password_hash
from models.user import User

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create_user(self, user: UserCreateRequest) -> UserCreateResponse:
        hashed_password = get_password_hash(user.password)
        user_data = user.model_dump(exclude={"password"})
        user_data["password"] = hashed_password
        return self.user_repo.create_user(user_data)

    def get_user(self, user_id: int) -> UserReadResponse:
        return UserReadResponse.model_validate(self.user_repo.get_user_by_id(user_id))

    def get_user_by_username(self, username: str) -> UserReadResponse:
        return UserReadResponse.model_validate(self.user_repo.get_user_by_username(username))

    def get_user_by_username_for_auth(self, username: str) -> User:
        return self.user_repo.get_user_by_username(username)

    def update_user(self, user_id: int, user: UserUpdateRequest) -> UserUpdateResponse:
        user_data = user.model_dump(exclude_unset=True)
        if "password" in user_data:
            user_data["password"] = get_password_hash(user_data["password"])
        return self.user_repo.update_user(user_id, user_data)

    def delete_user(self, user_id: int) -> UserDeleteResponse:
        self.user_repo.delete_user(user_id)
        return UserDeleteResponse(detail="User deleted")
