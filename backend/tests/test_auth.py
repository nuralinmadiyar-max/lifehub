import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 🔴 ВАЖНО: ДО import app
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from database import Base, get_db
import models
from main import app


engine = create_engine(
    "sqlite:///./test.db",
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_register_user():
    response = client.post(
        "/register",
        json={
            "email": "test@example.com",
            "password": "123456"
        }
    )
    assert response.status_code == 200
    assert "email" in response.json()


def test_login_user():
    response = client.post(
        "/login",
        data="username=test@example.com&password=123456",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()