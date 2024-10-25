from typing import Any
from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import User


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    async def create_user(self, values: dict[str, Any]):
        instance = User(**values)
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)

        return instance

    async def get_user_by_name(self, name: str) -> User | None:
        stmt = select(User).filter(User.username == name)
        instance = self.session.execute(stmt).scalar_one_or_none()

        return instance
