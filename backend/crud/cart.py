from sqlalchemy.orm import Session
from backend.models.cart import CartDB
from backend.schemas.cart import CartItemCreate


def get_products_in_cart(db: Session, skip: int = 0, limit: int = 10):
    return db.query(CartDB).offset(skip).limit(limit).all()


def add_product_to_cart(db: Session, product: CartItemCreate):
    db_cart = CartDB(name=product.name, quantity=product.quantity, purchased=False)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart


def soft_delete_cart_item(db: Session, product_id: int):
    db_cart = db.query(CartDB).filter(CartDB.id == product_id).first()
    if db_cart:
        db_cart.is_deleted = True
        db.commit()
        return db_cart
    return None


def undo_deletion(db: Session, product_id: int):
    db_cart = db.query(CartDB).filter(CartDB.id == product_id).first()
    if db_cart:
        db_cart.is_deleted = False
        db.commit()
        return db_cart
    return None
