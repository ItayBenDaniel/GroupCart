from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models.cart import CartDB
from backend.models.products import Product
from backend.schemas.cart import CartItemCreate, CartItemUpdate, CartItem
from backend.core.utils import get_current_user

router = APIRouter(prefix="/cart", tags=["cart"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=CartItem)
def add_to_cart(
    item: CartItemCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    # Optional: Check that product exists
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Create cart item
    db_item = CartDB(
        user_id=user_id,
        product_id=item.product_id,
        quantity=item.quantity,
        purchased=False
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/", response_model=list[CartItem])
def get_user_cart(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return db.query(CartDB).filter(CartDB.user_id == user_id).all()


@router.patch("/{item_id}", response_model=CartItem)
def update_cart_item(
    item_id: int,
    updates: CartItemUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    item = db.query(CartDB).filter(
        CartDB.id == item_id,
        CartDB.user_id == user_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if updates.quantity is not None:
        item.quantity = updates.quantity
    if updates.purchased is not None:
        item.purchased = updates.purchased

    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}")
def delete_cart_item(
    item_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    item = db.query(CartDB).filter(
        CartDB.id == item_id,
        CartDB.user_id == user_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()
    return {"detail": "Item removed from cart"}

