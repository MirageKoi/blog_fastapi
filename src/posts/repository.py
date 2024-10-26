from typing import Any, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Comment, Post


class PostRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    async def get_post_all(self) -> Sequence[Post]:
        stmt = select(Post)
        res = self.session.scalars(stmt).all()
        return res

    async def get_post_by_id(self, pk: int) -> Post | None:
        res = self.session.get(Post, pk)
        return res

    async def create_post(self, values: dict[str, Any]) -> Post:
        instance = Post(**values)
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)

        return instance

    async def update_post(self, db_post: Post, values: dict[str, Any]) -> Post:
        instance = db_post
        for k, v in values.items():
            setattr(instance, k, v)

        self.session.commit()

        return instance

    async def delete_post(self, db_post: Post) -> None:
        self.session.delete(db_post)
        self.session.commit()

    async def create_comment(self, values: dict[str, Any]):
        instance = Comment(**values)
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)

        return instance
