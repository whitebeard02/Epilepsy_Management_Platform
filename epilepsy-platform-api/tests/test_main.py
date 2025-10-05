# tests/test_main.py

from fastapi.testclient import TestClient

# The 'client' parameter comes from the fixture we defined in conftest.py
def test_read_root(client: TestClient):
    # Make a request to the root URL
    response = client.get("/")

    # Assert that the status code is 200 OK
    assert response.status_code == 200

    # Assert that the response body is what we expect
    assert response.json() == {"status": "API is running"}