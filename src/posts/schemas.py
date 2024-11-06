from __future__ import annotations

import datetime as dt

from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    content: str


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class PostResponseDB(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    created_at: dt.datetime

    comments: list[CommentResponseDB] | None = None


class PostCreateDB(BaseModel):
    title: str
    content: str
    user_id: int


class CommentCreate(BaseModel):
    content: str


class CommentCreateDB(CommentCreate):
    post_id: int
    user_id: int
    is_blocked: bool = False


class CommentResponseDB(BaseModel):
    id: int
    content: str
    post_id: int
    user_id: int
    created_at: dt.datetime
