from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models.cart import CartDB
from backend.models.store_product import StoreProduct
from backend.models.users import User
from backend.schemas.cart import CartItemCreate, CartItemUpdate, CartItem, CartProduct
from backend.core.utils import get_current_user
from typing import List

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
    # user_id: int = Depends(get_current_user),
):
    print("HERE1")
    if item.quantity <= 0:
        raise HTTPException(
            status_code=400, detail="Amount added needs to be greater than 0"
        )
    print("HERE2")

    # Optional: Check that product exists
    product = (
        db.query(StoreProduct).filter(StoreProduct.id == item.store_product_id).first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    print("HERE3")

    # Checking if item exists in cart
    existing_item = (
        db.query(CartDB)
        .filter_by(user_id=1, store_product_id=item.store_product_id, is_deleted=False)
        .first()
    )

    user = db.query(User).filter(User.id == 1).first()
    if not user.family_id:
        raise HTTPException(status_code=400, detail="User must belong to a family")
    print("HERE5")

    if existing_item:
        existing_item.quantity += item.quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item
    # Create cart item
    db_item = CartDB(
        user_id=1,
        store_product_id=item.store_product_id,
        family_id=user.family_id,
        quantity=item.quantity,
        purchased=False,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/", response_model=list[CartItem])
def get_user_cart(db: Session = Depends(get_db)):
    return db.query(CartDB).filter(CartDB.user_id == 1).all()


@router.get("/full", response_model=list)
def get_user_cart_full(
    db: Session = Depends(get_db),
):
    cart_items = (
        db.query(CartDB).filter(CartDB.user_id == 1, CartDB.is_deleted == False).all()
    )

    results = []
    for item in cart_items:
        product_data = (
            db.query(StoreProduct)
            .filter(StoreProduct.id == item.store_product_id)
            .first()
        )
        product_dict = {
            "id": product_data.id,
            "name": product_data.name,
            "price": product_data.price,
            "item_code": product_data.item_code,
            "unit_of_measure": product_data.unit_of_measure,
            "quantity": item.quantity,  # Add the quantity from cart
        }
        results.append(product_dict)

    return results


@router.get("/full2")
def get_user_cart_full():

    print("WOW")


@router.get("/{family_id}", response_model=list[CartItem])
def get_family_cart(
    family_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):

    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.family_id != family_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this family cart"
        )

    # Get all non-deleted items from this family's cart
    items = (
        db.query(CartDB)
        .filter(CartDB.family_id == family_id, CartDB.is_deleted == False)
        .all()
    )
    return items


@router.patch("/{item_id}", response_model=CartItem)
def update_cart_item(
    item_id: int,
    updates: CartItemUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    if updates.quantity < 0:
        raise HTTPException(
            status_code=400, detail="Amount added needs to be greater than 0"
        )

    item = (
        db.query(CartDB).filter(CartDB.id == item_id, CartDB.user_id == user_id).first()
    )

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if updates.quantity == 0:
        item.is_deleted = True
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
    user_id: int = Depends(get_current_user),
):
    item = (
        db.query(CartDB).filter(CartDB.id == item_id, CartDB.user_id == user_id).first()
    )

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()
    return {"detail": "Item removed from cart"}
