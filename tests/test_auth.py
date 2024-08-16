from fastapi.testclient import TestClient
from main import app  # Ensure this is the correct import path for your FastAPI application setup

client = TestClient(app)

def test_user_registration():
    registration_url = "/auth/register"
    registration_data = {
        "username": "johnsnow224",
        "email": "johnsnow24@yahoo.com",
        "password": "Johnsnow123"
    }
    response = client.post(registration_url, json=registration_data)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    # Add more assertions here as needed based on what your endpoint returns
