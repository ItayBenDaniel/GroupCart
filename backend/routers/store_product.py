from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import database
from backend.schemas.store_product import StoreProduct, StoreProductCreate
from backend.crud.store_product import get_num_of_store_products

router = APIRouter(prefix="/store_products", tags=["store_products"])


# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/random/{count}", response_model=list[StoreProduct])
def get_num_of_products(count: int, db: Session = Depends(get_db)):
    return get_num_of_store_products(count, db)
