import random
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct

from backend.database import SessionLocal
from backend.models.store_product import StoreProduct
from backend.models.store import Store
from backend.scrapper.image_extractor import (
    download_barcode_image,
)
import time
import random
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
MAX_PRODUCTS = 100


def main():
    db: Session = SessionLocal()
    subq = (
        db.query(StoreProduct.item_code)
        .join(Store, StoreProduct.store_id == Store.id)
        .filter(StoreProduct.has_image == False)
        .group_by(StoreProduct.item_code)
        .having(func.count(distinct(Store.chain_name)) > 1)
        .subquery()
    )

    products = (
        db.query(StoreProduct)
        .filter(StoreProduct.item_code.in_(subq))
        .filter(StoreProduct.has_image == False)
        .filter(StoreProduct.category != "אחר")
        .order_by(func.random())
        .limit(MAX_PRODUCTS)
        .all()
    )

    success = 0
    for product in products:
        time.sleep(random.uniform(1.0, 2.5))
        result = download_barcode_image(product.item_code)
        if result.startswith("Image saved"):
            product.has_image = True
            db.add(product)
            success += 1
            print(f"Image saved for {product.item_code}")
        else:
            print(f" error {product.item_code}")
    print(f"Successfully downloaded {success} out of {len(products)} images")
    db.commit()
    db.close()


if __name__ == "__main__":
    main()
