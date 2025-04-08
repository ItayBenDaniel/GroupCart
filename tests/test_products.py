# tests/test_products.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi.testclient import TestClient
from backend.main import app
import random

client = TestClient(app)


def test_create_product():
    unique_name = f"TestProduct{random.randint(1000, 9999)}"
    unique_price = random.randint(1, 100)
    product_data = {
        "name": unique_name,
        "description": "Test description",
        "category": "test category",
        "price": unique_price,
    }

    response = client.post("/products/", json=product_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["description"] == product_data["description"]
    assert data["price"] == product_data["price"]


def test_get_products():
    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
