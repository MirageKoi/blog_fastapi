import datetime as dt
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session

from src.adapters.database import get_db
from src.auth.routers import get_current_user
from src.auth.schemas import DecodedToken

from .models import Comment
from .repository import PostRepository
from .schemas import (
    CommentCreate,
    CommentCreateDB,
    CommentResponseDB,
    PostCreate,
    PostCreateDB,
    PostResponseDB,
    PostUpdate,
)

router = APIRouter(prefix="/post", tags=["posts"])


db_session = Annotated[Session, Depends(get_db)]
current_user = Annotated[DecodedToken, Depends(get_current_user)]


def get_repository(session: db_session):
    return PostRepository(session)


repository = Annotated[PostRepository, Depends(get_repository)]


@router.get("/", response_model=list[PostResponseDB])
async def get_post_list(repo: repository):
    response = await repo.get_post_all()

    return response


@router.get("/{id}", response_model=PostResponseDB)
async def get_post_by_id(id: int, repo: repository):
    response = await repo.get_post_by_id(id)
    return response


@router.post("/", response_model=PostResponseDB, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, user: current_user, repo: repository):
    new_post = PostCreateDB(**post.model_dump(), user_id=user.id)
    response = await repo.create_post(new_post.model_dump())

    return response


@router.put("/{id}", response_model=PostResponseDB)
async def update_post(id: int, post: PostUpdate, user: current_user, repo: repository):
    db_post = await repo.get_post_by_id(id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post has not been found.")
    if db_post.user_id != user.id:
        raise HTTPException(status_code=403, detail="You have no permissions.")

    response = await repo.update_post(db_post, post.model_dump(exclude_none=True))

    return response


@router.delete("/{id}")
async def delete_post(id: int, user: current_user, repo: repository):
    db_post = await repo.get_post_by_id(id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post has not been found.")
    if db_post.user_id != user.id:
        raise HTTPException(status_code=403, detail="You have no permissions.")

    await repo.delete_post(db_post)

    return {"status": "OK"}


@router.post("/{id}/comment", response_model=CommentResponseDB)
async def create_comment(
    id: int, repo: repository, user: current_user, item: CommentCreate
):
    if repo.get_post_by_id(id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post has not been found."
        )
    # TODO: Add AI moderation
    # is_valid = validate_context(item.content)
    new_comment = CommentCreateDB(content=item.content, post_id=id, user_id=user.id)
    response = await repo.create_comment(new_comment.model_dump())

    return response
