from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from backend.models.store import Store
from backend.schemas.store import StoreCreate


def get_store_by_store_id(db: Session, store_id: int) -> Store | None:
    return db.query(Store).filter(Store.store_id == store_id).first()


def create_store(db: Session, store: StoreCreate) -> Store:
    existing = get_store_by_store_id(db, store.store_id)
    if existing:
        return existing
    db_store = Store(
        store_id=store.store_id,
        chain_id=store.chain_id,
        chain_name=store.chain_name,
        name=store.name,
        address=store.address,
        city=store.city,
        latitude=store.latitude,
        longitude=store.longitude,
    )
    db.add(db_store)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(db_store)
    return db_store


def get_all_stores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Store).offset(skip).limit(limit).all()
