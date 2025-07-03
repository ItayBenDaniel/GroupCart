from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models.liked_items import LikedItem
from backend.models.store_product import StoreProduct
from backend import database
from backend.core.utils import get_current_user

router = APIRouter(prefix="/likes", tags=["likes"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{store_product_id}")
def like_item(
    store_product_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    existing = (
        db.query(LikedItem)
        .filter_by(user_id=user_id, store_product_id=store_product_id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Already liked")
    db.add(LikedItem(user_id=user_id, store_product_id=store_product_id))
    db.commit()
    return {"message": "Liked"}


@router.delete("/{store_product_id}")
def unlike_item(
    store_product_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    like = (
        db.query(LikedItem)
        .filter_by(user_id=user_id, store_product_id=store_product_id)
        .first()
    )
    if not like:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(like)
    db.commit()
    return {"message": "Unliked"}


@router.get("/")
def get_liked_items(
    db: Session = Depends(get_db), user_id: int = Depends(get_current_user)
):
    liked = (
        db.query(StoreProduct)
        .join(LikedItem, StoreProduct.id == LikedItem.store_product_id)
        .filter(LikedItem.user_id == user_id)
        .all()
    )
    return liked
