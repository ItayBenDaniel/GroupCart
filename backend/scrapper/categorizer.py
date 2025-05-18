import requests
from urllib.parse import quote_plus
from backend.database import SessionLocal
from backend.models.store_product import StoreProduct

API_KEY = "your_real_api_key_here"
API_BASE_URL = (
    "https://www.productcategorization.com/api/ecommerce/ecommerce_category6_get.php"
)


def get_category_from_api(name: str) -> str:
    encoded_name = quote_plus(name)
    url = f"{API_BASE_URL}?query={encoded_name}&api_key={API_KEY}"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            data = res.json()
            return data.get("classification", "")
        else:
            print(f"❌ Error {res.status_code} for '{name}': {res.text}")
            return ""
    except Exception as e:
        print(f"❌ Exception for '{name}': {e}")
        return ""


def test_product_categorization(limit=20):
    db = SessionLocal()
    products = (
        db.query(StoreProduct)
        .filter(
            StoreProduct.category == None
        )  # or .filter(StoreProduct.category == '')
        .limit(limit)
        .all()
    )
    for p in products:
        category = get_category_from_api(p.name)
        print(f"🔍 {p.name} → {category}")
    db.close()


if __name__ == "__main__":
    test_product_categorization()
