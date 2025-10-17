# tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base  # <-- CRITICAL: Imports the Base for table creation
from app.dependencies import get_db

# --- CRITICAL: Import all SQLAlchemy models ---
# This ensures that Base.metadata knows about all your tables.
from app.models import patient, clinician

# --- Test Database Setup ---
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Create all database tables before any tests run
    Base.metadata.create_all(bind=engine)
    yield
    # Drop all database tables after all tests have run
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    # Fixture to provide a test client with an overridden database dependency
    def override_get_db():
        database = TestingSessionLocal()
        try:
            yield database
        finally:
            database.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def authenticated_client(client: TestClient):
    # Fixture to provide a pre-authenticated test client
    client.post("/clinicians/", json={
        "email": "testauth@example.com",
        "password": "testpassword123"
    })

    login_response = client.post("/token", data={
        "username": "testauth@example.com",
        "password": "testpassword123"
    })
    token = login_response.json()["access_token"]

    client.headers["Authorization"] = f"Bearer {token}"

    return client