from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import database
from backend.crud.products import get_products, create_product  # ✅ Import functions from crud
from backend.schemas.products import Product, ProductCreate

router = APIRouter(prefix="/products", tags=["products"])

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[Product])
def get_products_route(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_products(db, skip=skip, limit=limit)

@router.post("/", response_model=Product)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    return get_products(db, product)