from fastapi.testclient import TestClient
from main import app  # Ensure this correctly points to where your FastAPI app is initialized

client = TestClient(app)

def test_read_movies():
    response = client.get("/movies")
    assert response.status_code == 200
    # Ensure the response is a list and check for expected content structure
    assert isinstance(response.json(), list)  # Checks that response is a list
    if response.json():
        # If there's data, you might want to test for the presence of expected keys
        assert "id" in response.json()[0]
        assert "title" in response.json()[0]

def test_user_registration():
    # Define the endpoint
    registration_url = "/auth/register"  # Adjust the URL based on your actual endpoint

    # Define a valid payload
    registration_data = {
        "username": "johnsnow24",
        "email": "johnsnow24@yahoo.com",
        "password": "johnsnow123"
    }

    # Send a POST request to the registration endpoint
    response = client.post(registration_url, json=registration_data)

    # Check that the response status code is 201 (Created) or another expected success code
    assert response.status_code == 201, "Expected status code 201, got {0}".format(response.status_code)

    # Check the response body if necessary
    # This depends on what your registration endpoint returns
    response_data = response.json()
    assert response_data["username"] == "johnsnow24", "Username in the response doesn't match the requested username"

    # Optional: Further checks can include checking the response for a token if your API returns one upon registration
    # and checking that the user was added to the database
