from typing import Any, Protocol

from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from src.posts.schemas import CommentResponseDB, PostResponseDB

from .models import Comment, Post


class IPostRepository(Protocol):
    async def get_post_all(self) -> list[PostResponseDB | None]: ...

    async def get_post_by_id(self, id: int) -> PostResponseDB | None: ...

    async def create_post(self, values: dict[str, Any]) -> PostResponseDB: ...

    async def update_post(self, id: int, values: dict[str, Any]) -> PostResponseDB: ...

    async def delete_post(self, id: int) -> None: ...

    async def create_comment(self, values: dict[str, Any]) -> CommentResponseDB: ...


class PostRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    async def get_post_all(self) -> list[PostResponseDB]:
        stmt = select(Post)
        res = self.session.scalars(stmt).all()
        return [PostResponseDB(**entity.__dict__) for entity in res]

    async def get_post_by_id(self, id: int) -> PostResponseDB | None:
        res = self.session.get(Post, id)
        if res:
            return PostResponseDB(**res.__dict__)
        else:
            return None

    async def create_post(self, values: dict[str, Any]) -> PostResponseDB:
        instance = Post(**values)
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)

        return PostResponseDB(**instance.__dict__)

    async def update_post(self, id: int, values: dict[str, Any]) -> PostResponseDB:
        stmt = update(Post).where(Post.id == id).values(**values).returning(Post)
        instance = self.session.scalar(stmt)

        return PostResponseDB.model_validate(instance.__dict__)

    async def delete_post(self, id: int) -> None:
        self.session.execute(delete(Post).where(Post.id == id))

    async def create_comment(self, values: dict[str, Any]) -> CommentResponseDB:
        instance = Comment(**values)
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)

        return CommentResponseDB.model_validate(instance.__dict__)
