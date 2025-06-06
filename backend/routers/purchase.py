from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from backend.core.utils import get_current_user
from typing import List
from backend.models.purchase import Purchase, PurchaseItem
from backend.schemas.purchase import PurchaseCreate, PurchaseOut
from backend import database
from backend.models.cart import CartDB
from backend.models.users import User

router = APIRouter(prefix="/purchases", tags=["Purchases"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=PurchaseOut)
def create_purchase(
    purchase_data: PurchaseCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    if not purchase_data.items:
        raise HTTPException(status_code=400, detail="No items to purchase")
    user = db.query(User).filter(User.id == user_id).first()
    if not user.family_id:
        raise HTTPException(status_code=400, detail="User must belong to a family")
    purchase = Purchase(family_id=user.family_id)
    db.add(purchase)
    db.flush()  # Get purchase.id before inserting items
    for item in purchase_data.items:
        db.add(
            PurchaseItem(
                purchase_id=purchase.id,
                product_id=item.product_id,
                quantity=item.quantity,
            )
        )
    db.query(CartDB).filter(CartDB.family_id == user.family_id).delete()
    db.commit()
    db.refresh(purchase)
    return purchase


@router.get("/", response_model=List[PurchaseOut])
def get_my_purchases(
    db: Session = Depends(get_db), user_id: int = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user.family_id:
        raise HTTPException(status_code=400, detail="User must belong to a family")
    print("YAYAYYAY")
    purchases = (
        db.query(Purchase)
        .options(joinedload(Purchase.items).joinedload(PurchaseItem.product))
        .filter(Purchase.family_id == user.family_id)
        .all()
    )
    print(f"PURCHASES ARE {purchases}")
    return purchases


@router.delete("/{purchase_id}")
def delete_purchase(
    purchase_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    item = db.query(Purchase).filter(Purchase.id == purchase_id).first()
    db.delete(item)
    db.commit()
    return f"Purchase id: {purchase_id} of user: {user_id} has been deleted"
