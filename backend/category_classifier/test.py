import json
import random
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models.store_product import StoreProduct


def get_random_uncategorized_products(limit=100):
    db: Session = SessionLocal()
    try:
        # Load all uncategorized product IDs and names (can be slow if millions — tweak if needed)
        results = (
            db.query(StoreProduct.id, StoreProduct.name)
            .filter(
                StoreProduct.category == "אחר",
                StoreProduct.name != None,
                StoreProduct.has_image == True,
            )
            .all()
        )
        # Shuffle and take `limit`
        sample = random.sample(results, min(limit, len(results)))
        return [{"id": row.id, "name": row.name} for row in sample]
    finally:
        db.close()


if __name__ == "__main__":
    limit = 500  # change as needed
    filename = f"batch_{limit}_products.json"

    batch = get_random_uncategorized_products(limit)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(batch, f, ensure_ascii=False, indent=2)

    print(f"✓ Wrote {len(batch)} products to: {filename}")
