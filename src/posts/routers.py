from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.adapters.database import get_db
from src.auth.routers import get_current_user
from src.auth.schemas import DecodedToken
from src.content_manager.client import ILanguageClient
from src.content_manager.dependecies import get_ai_client

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


moderator_dependency = Annotated[ILanguageClient, Depends(get_ai_client)]


@router.get("/", response_model=list[PostResponseDB])
async def get_post_list(repo: repository):
    response = await repo.get_post_all()

    return response


@router.get("/{id}", response_model=PostResponseDB)
async def get_post_by_id(id: int, repo: repository):
    response = await repo.get_post_by_id(id)
    return response


@router.post("/", response_model=PostResponseDB, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate,
    user: current_user,
    repo: repository,
    moderation: moderator_dependency,
):
    is_safe = moderation.analyze_text(post.content)
    if not is_safe:
        raise HTTPException(
            status_code=418,
            detail="Post contains zero tolerance and wont be published",
        )
    new_post = PostCreateDB(**post.model_dump(), user_id=user.id)
    response = await repo.create_post(new_post.model_dump())

    return response


@router.put("/{id}", response_model=PostResponseDB)
async def update_post(
    id: int,
    post: PostUpdate,
    user: current_user,
    repo: repository,
    moderation: moderator_dependency,
):
    db_post = await repo.get_post_by_id(id)
    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post has not been found.")
    if db_post.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no permissions.")
    if post.content is not None:
        is_safe = moderation.analyze_text(post.content)
        if not is_safe:
            raise HTTPException(
                status_code=status.HTTP_418_IM_A_TEAPOT,
                detail="Post contains zero tolerance and wont be published",
            )

    response = await repo.update_post(id, post.model_dump(exclude_none=True))

    return response


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, user: current_user, repo: repository):
    db_post = await repo.get_post_by_id(id)
    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post has not been found.")
    if db_post.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no permissions.")

    await repo.delete_post(id)

    return {"status": "OK"}


@router.post("/{id}/comment", response_model=CommentResponseDB)
async def create_comment(
    id: int,
    repo: repository,
    user: current_user,
    item: CommentCreate,
    moderation: moderator_dependency,
):
    if await repo.get_post_by_id(id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post has not been found.")
    new_comment = CommentCreateDB(content=item.content, post_id=id, user_id=user.id)
    if moderation.analyze_text(item.content) is False:
        new_comment.is_blocked = True

    response = await repo.create_comment(new_comment.model_dump())

    return response
