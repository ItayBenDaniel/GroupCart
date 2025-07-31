from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import database
from backend.models.family import Family
from backend.models.users import User
from backend.schemas.family import FamilyCreate, FamilyOut
from backend.core.utils import get_current_user
from typing import List
from datetime import datetime
from backend.models.purchase import Purchase, PurchaseItem
from backend.models.store_product import StoreProduct
from collections import defaultdict, Counter
from math import exp
from backend.models.cart import CartDB
from numpy import array


router = APIRouter(prefix="/family", tags=["Family"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=FamilyOut)
def create_family(
    family_data: FamilyCreate,
    db: Session = Depends(get_db),
    user_id=Depends(get_current_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if user.family_id is not None:
        raise HTTPException(status_code=400, detail="User already belnogs to a family")
    family = Family(name=family_data.name, owner_id=user_id)
    db.add(family)
    db.flush()

    user.family_id = family.id
    db.commit()
    db.refresh(family)
    return family


@router.get("/me", response_model=FamilyOut)
def get_my_family(
    db: Session = Depends(get_db), user_id: int = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.family:
        raise HTTPException(
            status_code=404, detail="User not found or doesnt belong to a family"
        )
    return user.family


@router.post("/{family_id}/join", response_model=FamilyOut)
def join_family(
    email: str,
    family_id: int,
    db: Session = Depends(get_db),
):
    family = db.query(Family).filter(Family.id == family_id).first()
    if not family:
        raise HTTPException(status_code=404, detail="Family not found")
    user = db.query(User).filter(User.email == email).first()
    user.family_id = family_id
    db.commit()
    db.refresh(user)
    return family


@router.get("/{family_id}", response_model=FamilyOut)
def get_family_by_id(
    family_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    family = db.query(Family).filter(Family.id == family_id).first()
    if not family:
        raise HTTPException(status_code=404, detail="Family not found")
    return family


@router.post("/{family_id}/leave")
def leave_family(
    family_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.family_id != family_id:
        raise HTTPException(status_code=400, detail="You are not in this family")

    user.family_id = None
    db.commit()
    return {"message": "Left family successfully"}
