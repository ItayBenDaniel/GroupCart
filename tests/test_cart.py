import random
import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def signup_and_login():
    signup_data = {
        "email": "user@example.com",
        "password": "string",
    }

    response = client.post(
        "/users/login",
        json={"email": signup_data["email"], "password": signup_data["password"]},
    )
    print("Login response:", response.status_code, response.json())  # Debug line

    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    return headers


def create_product():
    name = f"Product{random.randint(1000, 9999)}"
    product_data = {
        "name": name,
        "description": "Test product",
        "price": random.randint(1, 100),
        "category": "test",
    }
    response = client.post("/products/", json=product_data)
    return response.json()["id"]


def test_add_to_cart():
    headers = signup_and_login()
    product_id = create_product()

    response = client.post(
        "/cart/", json={"product_id": product_id, "quantity": 2}, headers=headers
    )
    assert response.status_code == 200
    assert response.json()["product_id"] == product_id
    assert response.json()["quantity"] == 2


def test_get_user_cart():
    headers = signup_and_login()
    product_id = create_product()
    client.post(
        "/cart/", json={"product_id": product_id, "quantity": 1}, headers=headers
    )

    response = client.get("/cart/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(item["product_id"] == product_id for item in response.json())


def test_update_cart_item():
    headers = signup_and_login()
    product_id = create_product()
    post_response = client.post(
        "/cart/", json={"product_id": product_id, "quantity": 1}, headers=headers
    )
    item_id = post_response.json()["id"]

    patch_response = client.patch(
        f"/cart/{item_id}", json={"quantity": 5}, headers=headers
    )
    assert patch_response.status_code == 200
    assert patch_response.json()["quantity"] == 5


def test_delete_cart_item():
    headers = signup_and_login()
    product_id = create_product()
    post_response = client.post(
        "/cart/", json={"product_id": product_id, "quantity": 1}, headers=headers
    )
    item_id = post_response.json()["id"]

    delete_response = client.delete(f"/cart/{item_id}", headers=headers)
    assert delete_response.status_code == 200
    assert delete_response.json()["detail"] == "Item removed from cart"
