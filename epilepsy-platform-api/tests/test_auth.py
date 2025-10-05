# tests/test_auth.py

from fastapi.testclient import TestClient

def test_create_clinician_success(client: TestClient):
    response = client.post("/clinicians/", json={
        "email": "test@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "hashed_password" not in data

def test_create_clinician_duplicate_email(client: TestClient):
    # This depends on the previous test having run and created the user
    response = client.post("/clinicians/", json={
        "email": "test@example.com",
        "password": "anotherpassword"
    })
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}

def test_login_success(client: TestClient):
    response = client.post("/token", data={
        "username": "test@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client: TestClient):
    response = client.post("/token", data={
        "username": "test@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect email or password"}

def test_access_protected_route_no_token(client: TestClient):
    response = client.get("/patients/")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_access_protected_route_with_token(client: TestClient):
    # First, log in to get a token
    login_response = client.post("/token", data={
        "username": "test@example.com",
        "password": "testpassword"
    })
    token = login_response.json()["access_token"]

    # Now, use the token to access the protected route
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/patients/", headers=headers)
    assert response.status_code == 200