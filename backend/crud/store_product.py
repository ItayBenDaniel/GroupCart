from sqlalchemy.orm import Session
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from backend.models.store_product import StoreProduct
from backend.schemas.store_product import StoreProductCreate
from backend.models.store import Store


def get_store_product_by_code(db: Session, item_code: str, store_id: int):
    return (
        db.query(StoreProduct)
        .filter(StoreProduct.item_code == str(item_code))
        .filter(StoreProduct.store_id == store_id)
        .first()
    )


def get_num_of_store_products(count: int, db: Session):

    subquery = (
        db.query(StoreProduct.item_code)
        .join(Store, StoreProduct.store_id == Store.id)
        .group_by(StoreProduct.item_code)
        .having(sa.func.count(sa.distinct(Store.chain_name)) > 1)
        .subquery()
    )
    return (
        db.query(StoreProduct)
        .filter(StoreProduct.item_code.in_(subquery))
        .filter(StoreProduct.has_image == True)
        .order_by(sa.func.random())
        .limit(count)
        .all()
    )


def create_store_product(db: Session, product: StoreProductCreate) -> StoreProduct:
    existing = get_store_product_by_code(db, product.item_code, product.store_id)
    if existing:
        return existing
    db_product = StoreProduct(
        store_id=product.store_id,
        item_code=product.item_code,
        name=product.name,
        manufacturer_name=product.manufacturer_name,
        manufacturer_country=product.manufacturer_country,
        item_description=product.item_description,
        unit_quantity=product.unit_quantity,
        unit_of_measure=product.unit_of_measure,
        quantity_in_package=product.quantity_in_package,
        price=product.price,
        discounted=product.discounted,
        has_image=False,
    )
    db.add(db_product)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(db_product)
    return db_product
