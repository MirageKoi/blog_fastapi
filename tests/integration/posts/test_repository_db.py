import pytest
from sqlalchemy import select
from src.posts.models import Post
from src.auth.models import User
from src.posts.repository import PostRepository


@pytest.fixture
def populated_session(session):
    u1 = User(username="bob", email="bob", password="bob")
    session.add(u1)
    session.commit()
    p1 = Post(title="Test 1", content="Test text", user_id=1)
    p2 = Post(title="Test 2", content="Test text", user_id=1)
    session.add_all([p1, p2])
    session.commit()

    yield session


async def test_retrive_all_posts(session):
    p1 = Post(title="Test 1", content="Test text", user_id=1)
    p2 = Post(title="Test 2", content="Test text", user_id=1)
    session.add_all([p1, p2])
    session.commit()

    repo = PostRepository(session)
    result = await repo.get_all()

    assert result
    assert len(result) == 2
    assert True


async def test_retrive_post_by_id(populated_session):
    repo = PostRepository(populated_session)

    result = await repo.get_by_id(2)

    assert result
    assert result.title == "Test 2"


async def test_create_post(session):
    repo = PostRepository(session)
    p1 = {"title": "Test 1", "content": "Test text", "user_id": 1}
    result = await repo.create(p1)

    record = session.scalar(select(Post))

    assert result
    assert result == record


async def test_update_post(populated_session):
    repo = PostRepository(populated_session)
    db_post = await repo.get_by_id(2)
    values_to_update = {"title": "Updated Title"}
    await repo.update(db_post, values_to_update)

    result = populated_session.get(Post, 2)

    assert result.title == "Updated Title"


async def test_delete_post(populated_session):
    repo = PostRepository(populated_session)
    db_post = await repo.get_by_id(2)
    await repo.delete(db_post)

    result = populated_session.scalar(select(Post).filter(Post.id == 2))

    assert result is None
