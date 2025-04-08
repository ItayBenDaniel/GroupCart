from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import database
from backend.models.family import Family
from backend.models.users import User
from backend.schemas.family import FamilyCreate, FamilyOut
from backend.core.utils import get_current_user
from typing import List

router = APIRouter(prefix="/families", tags=["families"])


router.post("/", response_model=FamilyOut)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


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


router.get("/me", response_model=List[FamilyOut])


def get_my_family(
    db: Session = Depends(get_db), user_id: int = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.family:
        raise HTTPException(
            status_code=404, detail="User not found or doesnt belong to a family"
        )
    return user.family


router.post("/join/{family_id}", response_model=FamilyOut)


def join_family(
    family_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    family = db.query(Family).filter(Family.id == family_id).first()
    if not family:
        raise HTTPException(status_code="404", detail="Family not found")
    user = db.query(User).filter(User.id == user_id).first()
    user.family_id = family_id
    db.commit
    return family
