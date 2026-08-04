import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key")
os.environ.setdefault("JWT_ALGORITHM", "HS256")
os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///./test.db")

from src.core.utils import generate_hashed_password
from src.database.sessions import get_db
from src.database.schemas import Base, User
from src.main import app

TEST_DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base.metadata.create_all(bind=engine)


def override_get_db() -> Generator:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def clear_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture(scope="session")
def test_client():
    return TestClient(app)


@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def register_user(client: TestClient, email: str = "user@example.com", password: str = "Password123!", username: str = "user1", phone_number: str | None = "1234567890", bio: str | None = "Test user"):
    payload = {
        "email": email,
        "password": password,
        "username": username,
        "phone_number": phone_number,
        "bio": bio,
    }
    return client.post("/app/auth/Register", json=payload)


def login_user(client: TestClient, email: str = "user@example.com", password: str = "Password123!"):
    return client.post("/app/auth/login", json={"email": email, "password": password})


def create_admin_user(db, email: str = "admin@example.com", password: str = "Password123!", username: str = "admin") -> User:
    hashed = generate_hashed_password(password)
    user = User(
        email=email,
        username=username,
        password=hashed,
        bio="Admin user",
        phone_number="1234567890",
        is_admin=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def user_token(test_client):
    response = register_user(test_client)
    assert response.status_code == 201
    login_response = login_user(test_client)
    assert login_response.status_code == 200
    return login_response.json()["access_token"]


@pytest.fixture
def admin_token(test_client, db_session):
    admin = create_admin_user(db_session)
    login_response = login_user(test_client, email=admin.email, password="Password123!")
    assert login_response.status_code == 200
    return login_response.json()["access_token"]
