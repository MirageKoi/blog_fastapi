from src.adapters.database import Base
# from src.adapters.models import Post
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    # posts: Mapped[list[Post]] = relationship()
    # comments: Mapped[list["Comment"]] = relationship(back_populates="user_id")

