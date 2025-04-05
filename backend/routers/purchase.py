from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.utils import get_current_user
from typing import List
from backend.models.purchase import Purchase, PurchaseItem
from backend.schemas.purchase import PurchaseCreate, PurchaseOut
from backend import database

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

    purchase = Purchase(user_id=user_id)
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

    db.commit()
    db.refresh(purchase)
    return purchase


@router.get("/", response_model=List[PurchaseOut])
def get_my_purchases(
    db: Session = Depends(get_db), user_id: int = Depends(get_current_user)
):
    return db.query(Purchase).filter(Purchase.user_id == user_id).all()


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
