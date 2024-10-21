import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from src.adapters.database import Base
from src.adapters.repositories import SQLAlchemyRepository
from src.adapters.models import User


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    with sessionmaker(bind=in_memory_db)() as session:
        yield session


def test_retrieve_records(session):
    users = [
        User(username=f"User {i}", email=f"test@email{i}", password="password")
        for i in range(1, 3)
    ]
    session.add_all(users)
    repo = SQLAlchemyRepository(User, session)

    result = repo.list()

    assert result == users


def test_retrieve_record_by_id(session):
    u1 = User(username="User 1", email="test@email1", password="password")
    u2 = User(username="User 2", email="test@email2", password="password")
    session.add_all([u1, u2])

    repo = SQLAlchemyRepository(User, session)
    result = repo.get(2)

    assert result.username == u2.username


def test_create_record(session):
    u1 = dict(username="User 1", email="test@email", password="password")
    repo = SQLAlchemyRepository(User, session)
    repo.create(u1)

    row = session.scalar(select(User))

    assert row.id == 1
    assert row.username == u1["username"]


def test_update_record(session):
    payload = dict(username="User 1", email="test@email", password="password")
    u1 = User(**payload)
    session.add(u1)
    session.commit()
    repo = SQLAlchemyRepository(User, session)
    repo.update(1, {"username": "User Update"})

    row = session.scalar(select(User))

    assert row.id == 1
    assert row.username == "User Update"


def test_delete_record(session):
    payload = dict(username="User 1", email="test@email", password="password")
    u1 = User(**payload)
    session.add(u1)
    session.commit()
    repo = SQLAlchemyRepository(User, session)
    repo.delete(1)

    row = session.scalar(select(User).where(User.username == "User 1"))

    assert row is None
