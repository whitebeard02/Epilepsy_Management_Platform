# tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base
from app.dependencies import get_db

# --- Test Database Setup ---
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- Pytest Fixture to Create and Drop Tables ---
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Create the database tables before any tests run
    Base.metadata.create_all(bind=engine)
    yield
    # Drop the database tables after all tests have run
    Base.metadata.drop_all(bind=engine)


# --- Pytest Fixture to Override DB Dependency and Provide a Test Client ---
@pytest.fixture
def client():
    # Dependency override: Use the test database instead of the main one
    def override_get_db():
        database = TestingSessionLocal()
        try:
            yield database
        finally:
            database.close()

    # Apply the override to the FastAPI app
    app.dependency_overrides[get_db] = override_get_db

    # Yield the TestClient for the tests to use
    yield TestClient(app)

    # Clean up the override after tests are done
    app.dependency_overrides.clear()
    # tests/conftest.py

# ... (keep all the existing code) ...

@pytest.fixture
def authenticated_client(client: TestClient):
    # Create a test clinician
    client.post("/clinicians/", json={
        "email": "testauth@example.com",
        "password": "testpassword123"
    })

    # Log in to get the token
    login_response = client.post("/token", data={
        "username": "testauth@example.com",
        "password": "testpassword123"
    })
    token = login_response.json()["access_token"]

    # Set the authorization header for the client
    client.headers["Authorization"] = f"Bearer {token}"

    return client