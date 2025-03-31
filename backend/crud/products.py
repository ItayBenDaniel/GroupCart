from sqlalchemy.orm import Session
from backend.models.products import Product  # ✅ Correct Import
from backend.schemas.products import ProductCreate  # ✅ Schema import for validation
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: ProductCreate):
    db_product = Product(
        name=product.name,
        description=product.description,
        category=product.category,
        price=product.price,
    )
    if product.name == "":
        raise HTTPException(
            status_code=400, detail="Product must have a valid non empty name"
        )
    if product.price < 0:
        raise HTTPException(
            status_code=400, detail="Product must have a valid non negative price"
        )

    try:
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Product already exists")
