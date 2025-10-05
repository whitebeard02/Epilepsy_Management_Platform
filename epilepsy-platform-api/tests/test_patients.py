# tests/test_patients.py

from fastapi.testclient import TestClient

# This test covers the entire successful lifecycle of a patient record
def test_patient_lifecycle(authenticated_client: TestClient):
    # 1. Create a new patient
    create_response = authenticated_client.post("/patients/", json={
        "full_name": "Test Patient",
        "date_of_birth": "2000-01-01",
        "clinician_id": 1
    })
    assert create_response.status_code == 201
    patient_data = create_response.json()
    patient_id = patient_data["id"]
    assert patient_data["full_name"] == "Test Patient"

    # 2. Read that specific patient to verify creation
    read_response = authenticated_client.get(f"/patients/{patient_id}")
    assert read_response.status_code == 200
    assert read_response.json()["full_name"] == "Test Patient"

    # 3. Update the patient
    update_response = authenticated_client.put(f"/patients/{patient_id}", json={
        "full_name": "Test Patient Updated"
    })
    assert update_response.status_code == 200
    assert update_response.json()["full_name"] == "Test Patient Updated"

    # 4. Delete the patient
    delete_response = authenticated_client.delete(f"/patients/{patient_id}")
    assert delete_response.status_code == 204

    # 5. Verify the patient is gone
    verify_delete_response = authenticated_client.get(f"/patients/{patient_id}")
    assert verify_delete_response.status_code == 404

# These tests cover the failure cases for non-existent patients
def test_read_nonexistent_patient(authenticated_client: TestClient):
    response = authenticated_client.get("/patients/99999")
    assert response.status_code == 404

def test_update_nonexistent_patient(authenticated_client: TestClient):
    response = authenticated_client.put("/patients/99999", json={"full_name": "ghost"})
    assert response.status_code == 404

def test_delete_nonexistent_patient(authenticated_client: TestClient):
    response = authenticated_client.delete("/patients/99999")
    assert response.status_code == 404