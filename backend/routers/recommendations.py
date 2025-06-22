from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models.users import User
from backend.models.purchase import Purchase, PurchaseItem
from backend.models.cart import CartDB
from backend.models.store_product import StoreProduct
from backend.core.utils import get_current_user
from sqlalchemy import func

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/family")
@router.get("/family")
def get_family_recommendations(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.family_id:
        raise HTTPException(status_code=400, detail="User must belong to a family")

    # Get product IDs currently in the cart (not purchased or deleted)
    cart_product_ids = (
        db.query(CartDB.store_product_id)
        .filter(
            CartDB.family_id == user.family_id,
            CartDB.purchased == False,
            CartDB.is_deleted == False,
        )
        .subquery()
    )

    # Top 10 previously purchased items not currently in the cart
    top_purchased_ids = (
        db.query(PurchaseItem.product_id, func.count(PurchaseItem.id).label("times"))
        .join(Purchase)
        .filter(Purchase.family_id == user.family_id)
        .filter(~PurchaseItem.product_id.in_(cart_product_ids))
        .group_by(PurchaseItem.product_id)
        .order_by(func.count(PurchaseItem.id).desc())
        .limit(10)
        .all()
    )

    product_ids = [pid for pid, _ in top_purchased_ids]

    recommended_products = (
        db.query(StoreProduct).filter(StoreProduct.id.in_(product_ids)).all()
    )

    return recommended_products
