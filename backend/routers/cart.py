from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models.cart import CartDB
from backend.models.store_product import StoreProduct
from backend.models.users import User
from backend.schemas.cart_change import CartChangeOut
from backend.schemas.cart import (
    CartItemCreate,
    CartItemUpdate,
    CartItem,
    BulkCartItem,
    BulkCartRequest,
)
from backend.core.utils import get_current_user
from typing import List
from backend.models.cart_change import CartChange
from datetime import datetime
from backend.models.store import Store
from haversine import haversine, Unit

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
    user_id: int = Depends(get_current_user),
):
    if item.quantity <= 0:
        raise HTTPException(
            status_code=400, detail="Amount added needs to be greater than 0"
        )

    # Optional: Check that product exists
    product = (
        db.query(StoreProduct).filter(StoreProduct.id == item.store_product_id).first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Checking if item exists in cart
    existing_item = (
        db.query(CartDB)
        .filter_by(
            user_id=user_id, store_product_id=item.store_product_id, is_deleted=False
        )
        .first()
    )

    user = db.query(User).filter(User.id == user_id).first()
    if not user.family_id:
        raise HTTPException(status_code=400, detail="User must belong to a family")

    if existing_item:
        existing_item.quantity += item.quantity
        db.commit()
        db.refresh(existing_item)
        db.add(
            CartChange(
                family_id=user.family_id,
                username=user.username,
                action="update",
                name=product.name,
                store_product_id=item.store_product_id,
                quantity=existing_item.quantity,
                previous_quantity=existing_item.quantity - item.quantity,
                timestamp=datetime.utcnow(),
                undone=0,
            )
        )
        db.commit()
        return existing_item
    # Create cart item
    db_item = CartDB(
        user_id=user_id,
        store_product_id=item.store_product_id,
        family_id=user.family_id,
        quantity=item.quantity,
        purchased=False,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    db.add(
        CartChange(
            family_id=user.family_id,
            username=user.username,
            action="add",
            name=product.name,
            store_product_id=item.store_product_id,
            quantity=item.quantity,
            previous_quantity=None,
            timestamp=datetime.utcnow(),
            undone=0,
        )
    )
    db.commit()
    return db_item


@router.get("/", response_model=list[CartItem])
def get_user_cart(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    return db.query(CartDB).filter(CartDB.user_id == user_id).all()


@router.get("/full", response_model=list)
def get_user_cart_full(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    cart_items = (
        db.query(CartDB)
        .filter(
            CartDB.family_id == user.family_id,
            CartDB.is_deleted == False,
            CartDB.purchased == False,
        )
        .all()
    )

    results = []
    for item in cart_items:
        product_data = (
            db.query(StoreProduct)
            .filter(StoreProduct.id == item.store_product_id)
            .first()
        )
        added_by_user = db.query(User).filter(User.id == item.user_id).first()
        print(f"item is {item}")
        print(f"user is {added_by_user.username}")
        if not added_by_user:
            added_by_username = "hh"
        else:
            added_by_username = added_by_user.username
        product_dict = {
            "id": product_data.id,
            "name": product_data.name,
            "price": product_data.price,
            "item_code": product_data.item_code,
            "unit_of_measure": product_data.unit_of_measure,
            "quantity": item.quantity,
            "added_by": added_by_username,
        }
        results.append(product_dict)

    return results


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


@router.patch("/{id}", response_model=CartItem)
def update_cart_item(
    id: int,
    item_update: CartItemUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    item = (
        db.query(CartDB)
        .filter(CartDB.store_product_id == id, CartDB.family_id == user.family_id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    old_quantity = item.quantity
    item.quantity = item_update.quantity
    if not item.quantity:
        raise HTTPException(status_code=400, detail="No quantity added")
    db.commit()
    db.refresh(item)
    user = db.query(User).filter(User.id == user_id).first()
    product = db.query(StoreProduct).filter(StoreProduct.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    # Log the update
    db.add(
        CartChange(
            family_id=item.family_id,
            name=product.name,
            username=user.username,
            action="update",
            store_product_id=item.store_product_id,
            quantity=item.quantity,
            previous_quantity=old_quantity,
            timestamp=datetime.utcnow(),
            undone=0,
        )
    )
    db.commit()
    return item


@router.delete("/{id}")
def delete_cart_item(
    id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    item = (
        db.query(CartDB)
        .filter(CartDB.store_product_id == id, CartDB.user_id == user_id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    user = db.query(User).filter(User.id == user_id).first()
    product = db.query(StoreProduct).filter(StoreProduct.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    # Log the delete before removing
    db.add(
        CartChange(
            family_id=item.family_id,
            username=user.username,
            name=product.name,
            action="delete",
            store_product_id=item.store_product_id,
            quantity=item.quantity,
            previous_quantity=item.quantity,
            timestamp=datetime.utcnow(),
            undone=0,
        )
    )

    db.delete(item)
    db.commit()

    return {"detail": "Item deleted"}


@router.patch("/{id}/mark_purchased")
def mark_item_as_purchased(
    id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    item = (
        db.query(CartDB)
        .filter(CartDB.store_product_id == id, CartDB.user_id == user_id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.purchased = True
    db.commit()
    return {"detail": "Marked as purchased"}


@router.post("/bulk", response_model=List[CartItem])
def bulk_add_to_cart(
    payload: BulkCartRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user.family_id:
        raise HTTPException(status_code=400, detail="User must belong to a family")

    added_items = []

    for item in payload.items:
        if item.quantity <= 0:
            continue

        product = (
            db.query(StoreProduct)
            .filter(StoreProduct.id == item.store_product_id)
            .first()
        )
        if not product:
            continue

        existing = (
            db.query(CartDB)
            .filter_by(
                user_id=user_id,
                store_product_id=item.store_product_id,
                is_deleted=False,
            )
            .first()
        )

        if existing:
            existing.quantity += item.quantity
            db.add(
                CartChange(
                    family_id=user.family_id,
                    username=user.username,
                    action="update",
                    name=product.name,
                    store_product_id=item.store_product_id,
                    quantity=existing.quantity,
                    previous_quantity=existing.quantity - item.quantity,
                    timestamp=datetime.utcnow(),
                    undone=0,
                )
            )
            added_items.append(existing)
        else:
            new_item = CartDB(
                user_id=user_id,
                family_id=user.family_id,
                store_product_id=item.store_product_id,
                quantity=item.quantity,
                purchased=False,
            )
            db.add(new_item)
            db.flush()
            db.add(
                CartChange(
                    family_id=user.family_id,
                    username=user.username,
                    action="add",
                    name=product.name,
                    store_product_id=item.store_product_id,
                    quantity=item.quantity,
                    previous_quantity=None,
                    timestamp=datetime.utcnow(),
                    undone=0,
                )
            )
            added_items.append(new_item)

    db.commit()
    return added_items


@router.get("/prices/compare")
def compare_cart_prices(
    lat: float,
    lon: float,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    # Get user's family and cart items
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.family_id:
        return {"error": "User must belong to a family"}
    radius_km = user.radius_km
    cart_items = (
        db.query(CartDB)
        .filter(
            CartDB.family_id == user.family_id,
            CartDB.is_deleted == False,
            CartDB.purchased == False,
        )
        .all()
    )

    if not cart_items:
        return {"error": "No active cart items found"}

    # Get nearby stores
    all_stores = (
        db.query(Store)
        .filter(Store.latitude.isnot(None), Store.longitude.isnot(None))
        .all()
    )

    results = []

    for store in all_stores:
        try:
            dist = haversine(
                (lat, lon),
                (float(store.latitude), float(store.longitude)),
                unit=Unit.KILOMETERS,
            )
            if dist > radius_km:
                continue

            # Try to price the cart in this store
            total = 0
            found_all = True

            for item in cart_items:
                store_product = (
                    db.query(StoreProduct)
                    .filter(
                        StoreProduct.item_code == item.store_product.item_code,
                        StoreProduct.store_id == store.id,
                    )
                    .first()
                )
                if not store_product:
                    found_all = False
                    break
                total += float(store_product.price) * item.quantity

            if found_all:
                results.append(
                    {
                        "store_id": store.id,
                        "store_name": store.name,
                        "chain_id": store.chain_id,
                        "address": store.address,
                        "distance_km": round(dist, 2),
                        "total_price": round(total, 2),
                    }
                )

        except Exception as e:
            continue

    results.sort(key=lambda x: x["total_price"])
    return results
