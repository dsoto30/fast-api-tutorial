import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.config import settings
from app.database import get_db
from app.models import Base
from app.oauth2 import create_access_token


# Use a dedicated test database so we never touch the development data.
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg://{settings.database_username}:{settings.database_password}"
    f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autoflush=False, bind=engine)


@pytest.fixture()
def session():
    """Provide a clean database session with fresh tables for each test."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    """A TestClient whose get_db dependency uses the test session."""

    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture()
def test_user(client):
    """Create a user through the API and return its data (with the password)."""
    user_data = {
        "email": "test@example.com",
        "password": "password123",
        "phone_number": "+14155552671",
    }
    res = client.post("/users", json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture()
def token(test_user):
    """A signed JWT access token for the created test user."""
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture()
def authorized_client(client, token):
    """A TestClient that sends the Authorization header for the test user."""
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}",
    }
    return client
