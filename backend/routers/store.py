from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.schemas.store import Store as StoreSchema
from backend.schemas.store_product import StoreProduct
from backend.models.store import Store
from backend.models.store_product import StoreProduct as StoreProductDB
from backend import database

router = APIRouter(prefix="/stores", tags=["stores"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[StoreSchema])
def get_stores(db: Session = Depends(get_db)):
    return db.query(Store).all()


@router.get("/{store_id}/products", response_model=list[StoreProduct])
def get_store_products(store_id: int, db: Session = Depends(get_db)):
    products = (
        db.query(StoreProductDB).filter(StoreProductDB.store_id == store_id).all()
    )
    if not products:
        raise HTTPException(status_code=404, detail="No products found for this store.")
    return products
