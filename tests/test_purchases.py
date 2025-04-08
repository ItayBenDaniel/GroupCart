import pytest
from fastapi.testclient import TestClient
from backend.main import app
import random

client = TestClient(app)


def signup_and_login():
    data = {
        "email": "user@example.com",
        "password": "string",
    }
    login_res = client.post(
        "/users/login", json={"email": data["email"], "password": data["password"]}
    )
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def create_product():
    product_data = {
        "name": f"Product{random.randint(1000, 9999)}",
        "description": "test",
        "category": "test",
        "price": 10,
    }
    res = client.post("/products/", json=product_data)
    return res.json()["id"]


def add_to_cart(product_id, headers):
    return client.post(
        "/cart/", json={"product_id": product_id, "quantity": 2}, headers=headers
    )


def test_create_purchase():
    headers = signup_and_login()
    product_id = create_product()
    add_to_cart(product_id, headers)

    purchase_payload = {"items": [{"product_id": product_id, "quantity": 2}]}

    res = client.post("/purchases/", json=purchase_payload, headers=headers)
    assert res.status_code == 200
    assert "id" in res.json()
    assert len(res.json()["items"]) == 1
    assert res.json()["items"][0]["product_id"] == product_id


def test_get_purchases():
    headers = signup_and_login()
    product_id = create_product()
    add_to_cart(product_id, headers)

    purchase_payload = {"items": [{"product_id": product_id, "quantity": 1}]}

    client.post("/purchases/", json=purchase_payload, headers=headers)
    res = client.get("/purchases/", headers=headers)

    assert res.status_code == 200
    assert isinstance(res.json(), list)
    assert len(res.json()) > 0
