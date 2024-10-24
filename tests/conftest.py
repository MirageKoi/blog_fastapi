import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.adapters.database import Base


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    with sessionmaker(bind=in_memory_db)() as session:
        yield session