from fastapi import HTTPException
from .repository import PostRepository


class PostService:
    def __init__(self, repository: PostRepository) -> None:
        self.repo = repository


    async def create_comment(self, post_id: int, user_id: int, comment_data):
        post = await self.repo.get_post_by_id(post_id)
        if post is None:
            raise HTTPException(None)
