from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models.store_product import StoreProduct
from .hybrid_classifier import hybrid_classify
import pandas as pd


# 1. Fetch up to 1000 products with non-null names
def fetch_products_for_classification(db: Session, limit: int = 10000):
    return db.query(StoreProduct).filter(StoreProduct.name != None).limit(limit).all()


# 2. Classify and update their 'category' field
def classify_and_update_categories():
    db = SessionLocal()

    try:
        products = fetch_products_for_classification(db)
        df = pd.DataFrame([{"id": p.id, "name": p.name} for p in products])

        if df.empty:
            print("No products to classify.")
            return

        df = hybrid_classify(df)

        updated_count = 0
        for _, row in df.iterrows():
            if row["category"] != "אחר":
                db.query(StoreProduct).filter(StoreProduct.id == row["id"]).update(
                    {StoreProduct.category: row["category"]}
                )
                updated_count += 1

        db.commit()
        print(f"✓ Updated {updated_count} products with new categories.")

    except Exception as e:
        db.rollback()
        print("❌ Error during classification:", e)
    finally:
        db.close()


if __name__ == "__main__":
    classify_and_update_categories()
