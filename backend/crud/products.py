from sqlalchemy.orm import Session
from backend.models.products import Product  # ✅ Correct Import
from backend.schemas.products import ProductCreate  # ✅ Schema import for validation

def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: ProductCreate):
    db_product = Product(name=product.name, quantity=product.quantity, purchased=False)  
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product