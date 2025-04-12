import random
from fastapi.testclient import TestClient
from backend.main import app  # adjust the import if needed

client = TestClient(app)


def signup_and_login():
    unique_username = f"user_{random.randint(1000, 9999)}"
    signup_data = {
        "username": unique_username,
        "email": f"{unique_username}@example.com",
        "password": "test123",
    }
    client.post("/users/signup", json=signup_data)
    login_data = {
        "email": signup_data["email"],
        "password": signup_data["password"],
    }
    response = client.post("/users/login", json=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def create_family(headers):
    return client.post(
        "/family/", json={"name": f"Fam_{random.randint(1000, 9999)}"}, headers=headers
    )


def test_create_family():
    headers = signup_and_login()
    response = create_family(headers)
    assert response.status_code == 200
    assert "id" in response.json()


def test_get_family():
    headers = signup_and_login()
    created = create_family(headers)
    family_id = created.json()["id"]
    response = client.get(f"/family/{family_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == family_id


def test_join_family():
    owner_headers = signup_and_login()
    created = create_family(owner_headers)
    family_id = created.json()["id"]

    new_user_headers = signup_and_login()
    response = client.post(f"/family/{family_id}/join", headers=new_user_headers)
    assert response.status_code == 200
    assert response.json()["id"] == family_id


def test_leave_family():
    headers = signup_and_login()
    created = create_family(headers)
    family_id = created.json()["id"]
    client.post(f"/family/{family_id}/join", headers=headers)
    response = client.post(f"/family/{family_id}/leave", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Left family successfully"
