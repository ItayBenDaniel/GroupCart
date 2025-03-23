from fastapi.testclient import TestClient
from backend.main import app
import random


client = TestClient(app)

# Unique test user
test_user = {
    "username": "testuser4",
    "email": "testuser4@example.com",
    "password": "test1234"
}

def test_signup():
    # Sign up can fail if already exists, so ignore 400 as valid
    response = client.post("/users/signup", json=test_user)
    assert response.status_code in [200, 400]

def test_signup_login_update_user():
    unique_username = f"user_{random.randint(1000, 9999)}"
    test_data = {
        "username": unique_username,
        "email": f"{unique_username}@example.com",
        "password": "test123"
    }

    # Signup
    signup_response = client.post("/users/signup", json=test_data)
    assert signup_response.status_code == 200  # ✅ Make sure user was created

    # Login
    response = client.post("/users/login", json={
        "email": test_data["email"],
        "password": test_data["password"]
    })
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Update
    headers = {"Authorization": f"Bearer {token}"}
    new_name = f"{unique_username}_updated"
    response = client.patch("/users/update", json={"username": new_name}, headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == new_name
