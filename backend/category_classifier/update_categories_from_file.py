import json
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models.store_product import StoreProduct


def update_categories_from_file(json_path: str):
    # Load the labeled categories
    with open(json_path, "r", encoding="utf-8") as f:
        labeled = json.load(f)
        print(labeled)

    db: Session = SessionLocal()
    updated_count = 0

    try:
        for entry in labeled:
            product_id = entry["id"]
            new_category = entry["category"]
            print("HERE")
            print(product_id)
            print(new_category)
            # Skip "אחר" (optional — in case some are left unlabeled)
            if new_category == "אחר":
                continue

            db.query(StoreProduct).filter(StoreProduct.id == product_id).update(
                {StoreProduct.category: new_category}
            )
            updated_count += 1

        db.commit()
        print(f"✓ Updated {updated_count} products.")
    except Exception as e:
        db.rollback()
        print("❌ Error updating categories:", e)
    finally:
        db.close()


if __name__ == "__main__":
    update_categories_from_file("gem.json")  # 👈 change this if needed
