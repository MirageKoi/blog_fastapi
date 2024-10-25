import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.adapters.database import Base, get_db
from src.auth.routers import get_current_user
from src.auth.schemas import DecodedToken
from src.main import app


# def override_get_current_user():
#     return DecodedToken(id=1, username="testuser", email="testemail")


# @pytest.fixture
# def api_session():
#     engine = create_engine(
#         "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
#     )
#     Base.metadata.create_all(engine)
#     with sessionmaker(engine, autocommit=False, autoflush=False)() as session:
#         yield session


# @pytest.fixture(name="client")
# def client_fixture(api_session: Session):
#     def get_session_override():
#         return api_session

#     app.dependency_overrides[get_db] = get_session_override
#     app.dependency_overrides[get_current_user] = override_get_current_user

#     client = TestClient(app)
#     yield client
#     app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_post_list(client):
    response = client.get("/post/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_post_by_id(client):
    post_data = {"title": "Test Post", "content": "This is a test post."}
    create_response = client.post("/post", json=post_data)
    created_post = create_response.json()
    post_id = created_post["id"]
    response = client.get(f"/post/{post_id}")
    assert response.status_code == 200
    assert response.json()["id"] == created_post["id"]


@pytest.mark.asyncio
async def test_create_post(client):
    post_data = {"title": "Test Post", "content": "This is a test post."}
    response = client.post("/post", json=post_data)
    assert response.status_code == 201
    created_post = response.json()
    assert created_post["title"] == "Test Post"
    assert created_post["content"] == "This is a test post."


@pytest.mark.asyncio
async def test_update_post(client):
    post_data = {"title": "Test Post", "content": "This is a test post."}
    create_response = client.post("/post/", json=post_data)
    created_post = create_response.json()

    update_data = {"title": "Updated Title", "content": "Updated content"}
    update_response = client.put(f"/post/{created_post['id']}", json=update_data)
    assert update_response.status_code == 200
    updated_post = update_response.json()
    assert updated_post["title"] == "Updated Title"


@pytest.mark.asyncio
async def test_delete_post(client):
    post_data = {"title": "Test Post", "content": "This is a test post."}
    create_response = client.post("/post/", json=post_data)
    created_post = create_response.json()

    delete_response = client.delete(f"/post/{created_post['id']}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"status": "OK"}
