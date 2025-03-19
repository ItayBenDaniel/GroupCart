from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import database
from backend.crud.items import get_items, create_item  # ✅ Import functions from crud
from backend.schemas.items import Item, ItemCreate

router = APIRouter(prefix="/items", tags=["items"])

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[Item])
def get_items_route(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_items(db, skip=skip, limit=limit)

@router.post("/", response_model=Item)
def add_item(item: ItemCreate, db: Session = Depends(get_db)):
    return create_item(db, item)