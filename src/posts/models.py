from __future__ import annotations

import datetime as dt

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.adapters.database import Base


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str]
    content: Mapped[str]
    created_at: Mapped[dt.datetime] = mapped_column(server_default=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        primaryjoin="and_(Comment.post_id == Post.id, Comment.is_blocked == False)",
        back_populates="post",
        cascade="all, delete-orphan",
    )


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    content: Mapped[str]
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[dt.datetime] = mapped_column(server_default=func.now())
    is_blocked: Mapped[bool] = mapped_column(default=False)

    post: Mapped["Post"] = relationship("Post", back_populates="comments")
