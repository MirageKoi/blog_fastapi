from sqlalchemy import select
from src.auth.repository import UserRepository
from src.auth.models import User


async def test_retrieve_valid_record_by_name(session):
    u1 = User(username="User 1", email="test@email1", password="password")
    u2 = User(username="User 2", email="test@email2", password="password")
    session.add_all([u1, u2])

    repo = UserRepository(session)
    result = await repo.get_user_by_name("User 2")

    assert result
    assert result.username == u2.username


async def test_try_to_retrive_nonexistent_record(session):
    u1 = User(username="User 1", email="test@email1", password="password")
    u2 = User(username="User 2", email="test@email2", password="password")
    session.add_all([u1, u2])

    repo = UserRepository(session)
    result = await repo.get_user_by_name("INVALID")

    assert result is None


async def test_create_record(session):
    u1 = dict(username="User 1", email="test@email", password="password")
    repo = UserRepository(session)
    await repo.create_user(u1)

    row = session.scalar(select(User))

    assert row
    assert row.id == 1
    assert row.username == u1["username"]
