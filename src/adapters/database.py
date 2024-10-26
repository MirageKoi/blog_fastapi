from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# from .config import settings

# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
SQLITE_URL = f"sqlite:///test.db"

engine = create_engine(SQLITE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    with SessionLocal() as session:
        try:
            yield session
        except Exception as exc:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
            )
        else:
            session.commit()
