# geocode_google.py
import time
import requests
from backend.database import SessionLocal
from backend.models.store import Store

GOOGLE_API_KEY = (
    "AIzaSyD9xjZgBx5wAr-BZRMbndrbngf8gSKi5Ic"  # 🔁 Replace with your actual key
)
GOOGLE_GEOCODER_URL = "https://maps.googleapis.com/maps/api/geocode/json"


def geocode_with_google(zip_code: str, name: str) -> tuple[str, str] | None:
    query = f"{zip_code}, {name}, ישראל"

    params = {"address": query, "key": GOOGLE_API_KEY}

    try:
        response = requests.get(GOOGLE_GEOCODER_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if data["status"] == "OK":
            location = data["results"][0]["geometry"]["location"]
            return str(location["lat"]), str(location["lng"])
        else:
            print(f"❌ Google API error: {data['status']} for '{query}'")
    except Exception as e:
        print(f"❌ Exception during geocoding '{query}': {e}")
    return None


def geocode_stores_by_zip_and_name_google():
    db = SessionLocal()
    stores = (
        db.query(Store)
        .filter(
            ((Store.latitude == "") | (Store.latitude == None))
            & ((Store.zip_code != "") & (Store.zip_code != "0000000"))
        )
        .all()
    )
    print(f"🧭 Found {len(stores)} stores to geocode with Google...")

    seen = set()

    for store in stores:
        query_key = (store.zip_code, store.name)
        if query_key in seen:
            print(f"⚠️ Skipping duplicate query for: {store.name}, {store.zip_code}")
            continue
        seen.add(query_key)

        coords = geocode_with_google(store.zip_code, store.name)
        if coords:
            lat, lon = coords
            store.latitude = lat
            store.longitude = lon
            print(f"📍 {store.name} ({store.zip_code}): {lat}, {lon}")
        else:
            print(f"⚠️ Could not geocode: {store.name}, {store.zip_code}")

        time.sleep(0.25)  # 4 requests/sec is safe

    db.commit()
    db.close()
    print("✅ Google geocoding complete.")


if __name__ == "__main__":
    geocode_stores_by_zip_and_name_google()
