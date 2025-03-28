from sqlalchemy.orm import Session
from backend.models.cart import CartItem  # ✅ Correct Import
from backend.schemas.cart import CartItemCreate  # ✅ Schema import for validation

def get_products_in_cart(db: Session, skip: int = 0, limit: int = 10):
    return db.query(CartItem).offset(skip).limit(limit).all()

def add_product_to_cart(db: Session, product: CartItemCreate):
    db_cart = CartItem(name=product.name, quantity=product.quantity, purchased=False)  
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart