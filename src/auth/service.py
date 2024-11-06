from passlib.context import CryptContext

from .repository import UserRepository
from .schemas import CreateUserRequest

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def create_user(self, user: CreateUserRequest):
        user.password = bcrypt_context.hash(user.password)
        user_info = user.model_dump()

        result = await self.repository.create_user(user_info)

        return result

    async def authenticate_user(self, username: str, password: str):
        user = await self.repository.get_user_by_name(username)
        if not user:
            return False
        if not bcrypt_context.verify(password, user.password):
            return False

        return user
