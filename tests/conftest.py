import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.adapters.database import Base, get_db
from src.auth.routers import get_current_user
from src.auth.schemas import DecodedToken
from src.main import app


def override_get_current_user():
    return DecodedToken(id=1, username="testuser", email="testemail")


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    with sessionmaker(bind=in_memory_db)() as session:
        yield session


@pytest.fixture
def api_session():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    with sessionmaker(engine, autocommit=False, autoflush=False)() as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(api_session: Session):
    def get_session_override():
        return api_session

    app.dependency_overrides[get_db] = get_session_override
    app.dependency_overrides[get_current_user] = override_get_current_user

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
