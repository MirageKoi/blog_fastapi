import datetime as dt
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session

from src.adapters.database import get_db
from src.posts.models import Comment

router = APIRouter(prefix="/analytics", tags=["analytics"])

db_session = Annotated[Session, Depends(get_db)]


class TotalCommentsOverTime(BaseModel):
    date: datetime
    total_comments: int
    blocked_comments: int


class CustomQuery(BaseModel):
    date_from: datetime = Field(default_factory=dt.date.today)
    date_to: datetime = Field(
        default_factory=lambda: dt.date.today() + dt.timedelta(days=1)
    )


filter_query = Annotated[CustomQuery, Query()]
# TODO: Separate bussiness logic from controller level
# Right now implementation is tightly coupled to specific storage (SQLAlchemy)
# In future we could separate this 
@router.get("/api/comments-daily-breakdown", response_model=list[TotalCommentsOverTime])
def comments_daily_breakdown(db: db_session, filter: filter_query):
    stmt = (
        select(
            func.date(Comment.created_at).label("date"),
            func.count(Comment.id).label("total_comments"),
            func.count(func.nullif(Comment.is_blocked, False)).label(
                "blocked_comments"
            ),
        )
        .filter(
            and_(
                Comment.created_at >= filter.date_from,
                Comment.created_at <= filter.date_to,
            )
        )
        .group_by(func.date(Comment.created_at))
        .order_by(func.date(Comment.created_at))
    )
    daily_comments = db.execute(stmt).all()

    return [
        TotalCommentsOverTime(
            date=result.date,
            total_comments=result.total_comments,
            blocked_comments=result.blocked_comments,
        )
        for result in daily_comments
    ]
