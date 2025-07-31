from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import database
from backend.schemas.store_product import StoreProduct, StoreProductCreate
from backend.crud.store_product import get_num_of_store_products
from backend.models.store import Store
from backend.models.store_product import StoreProduct as StoreProductDB
from random import random
from haversine import haversine, Unit

router = APIRouter(prefix="/store_products", tags=["store_products"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/random/{count}", response_model=list[StoreProduct])
def get_num_of_products(count: int, db: Session = Depends(get_db)):
    return get_num_of_store_products(count, db)


@router.get("/nearby_stores_with_product")
def nearby_stores_with_product(
    item_code: str,
    lat: float,
    lon: float,
    db: Session = Depends(get_db),
):
    from haversine import haversine, Unit

    print("STORE PRODUCT IS {}")
    store_products = (
        db.query(StoreProductDB)
        .filter(StoreProductDB.item_code == item_code)
        .join(Store)
        .filter(Store.latitude.isnot(None), Store.longitude.isnot(None))
        .all()
    )

    results = []
    for sp in store_products:
        store = sp.store
        try:
            dist = haversine(
                (lat, lon),
                (float(store.latitude), float(store.longitude)),
                unit=Unit.KILOMETERS,
            )
            results.append(
                {
                    "store_id": store.id,
                    "store_name": store.name,
                    "address": store.address,
                    "distance_km": round(dist, 2),
                    "price": float(sp.price),
                    "chain_id": store.chain_id,
                }
            )
        except Exception:
            continue

    results.sort(key=lambda x: x["distance_km"])
    return results[:5]


@router.get("/sales/nearby", response_model=list[StoreProduct])
def get_sales_nearby(
    lat: float = 31.90207111149355,
    lon: float = 35.01350010674653,
    limit: int = 50,
    db: Session = Depends(get_db),
):

    store_products = (
        db.query(StoreProductDB)
        .filter(
            StoreProductDB.promotion_price.isnot(None), StoreProductDB.has_image == True
        )
        .join(Store)
        .filter(Store.latitude.isnot(None), Store.longitude.isnot(None))
        .all()
    )

    nearby = []
    for sp in store_products:
        try:
            dist = haversine(
                (lat, lon),
                (float(sp.store.latitude), float(sp.store.longitude)),
                unit=Unit.KILOMETERS,
            )
            if dist <= 2000:
                nearby.append(sp)
        except:
            continue
    return nearby[:limit]
