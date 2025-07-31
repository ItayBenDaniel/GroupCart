from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from backend.database import SessionLocal

from backend.models.cart_change import CartChange
from backend.models.cart import CartDB
from backend.schemas.cart_change import CartChangeCreate, CartChangeOut
from backend.core.utils import get_current_user
from backend.models.users import User

router = APIRouter(prefix="/history", tags=["cart history"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/change", response_model=CartChangeOut)
def log_cart_change(change: CartChangeCreate, db: Session = Depends(get_db)):
    new_change = CartChange(
        **change.model_dump(), timestamp=datetime.utcnow(), undone=0
    )
    db.add(new_change)
    db.commit()
    db.refresh(new_change)
    return new_change


@router.get("/", response_model=list[CartChangeOut])
def get_cart_history(
    db: Session = Depends(get_db), user_id: int = Depends(get_current_user)
):
    print("HELLO")
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.family_id:
        raise HTTPException(status_code=400, detail="User must be in a family.")

    return (
        db.query(CartChange)
        .filter(CartChange.family_id == user.family_id)
        .order_by(CartChange.timestamp.desc())
        .all()
    )


@router.post("/undo", response_model=CartChangeOut)
def undo_last_change(
    db: Session = Depends(get_db), user_id: int = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == user_id).first()
    last_change = (
        db.query(CartChange)
        .filter(CartChange.family_id == user.family_id, CartChange.undone == 0)
        .order_by(CartChange.timestamp.desc())
        .first()
    )
    if not last_change:
        raise HTTPException(status_code=404, detail="No changes to undo")

    if last_change.action == "add":
        db.query(CartDB).filter(
            CartDB.family_id == last_change.family_id,
            CartDB.store_product_id == last_change.store_product_id,
        ).delete()
    elif last_change.action == "delete":
        user_change = (
            db.query(User).filter(User.username == last_change.username).first()
        )
        db.add(
            CartDB(
                family_id=user_change.family_id,
                user_id=user_change.id,
                store_product_id=last_change.store_product_id,
                quantity=last_change.quantity,
                purchased=False,
            )
        )
    elif last_change.action == "update":
        db.query(CartDB).filter(
            CartDB.family_id == last_change.family_id,
            CartDB.store_product_id == last_change.store_product_id,
        ).update({"quantity": last_change.previous_quantity})

    last_change.undone = 1
    db.commit()
    return last_change


# Redo the last undone change
@router.post("/redo", response_model=CartChangeOut)
def redo_last_undone(
    db: Session = Depends(get_db), user_id: int = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == user_id).first()
    undone = (
        db.query(CartChange)
        .filter(CartChange.family_id == user.family_id, CartChange.undone == 1)
        .order_by(CartChange.timestamp.asc())
        .first()
    )
    if not undone:
        raise HTTPException(status_code=404, detail="No changes to redo")
    change_user = db.query(User).filter(User.username == undone.username).first()
    if not change_user:
        raise HTTPException(status_code=404, detail="No user made the change")
    # Reapply action
    if undone.action == "add":
        db.add(
            CartDB(
                family_id=undone.family_id,
                user_id=change_user.id,
                store_product_id=undone.store_product_id,
                quantity=undone.quantity,
                purchased=False,
            )
        )
    elif undone.action == "delete":
        db.query(CartDB).filter(
            CartDB.family_id == undone.family_id,
            CartDB.store_product_id == undone.store_product_id,
        ).delete()
    elif undone.action == "update":
        db.query(CartDB).filter(
            CartDB.family_id == undone.family_id,
            CartDB.store_product_id == undone.store_product_id,
        ).update({"quantity": undone.quantity})

    undone.undone = 0
    db.commit()
    return undone
