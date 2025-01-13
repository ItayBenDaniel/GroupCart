from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import crud, database
from backend.schemas import items

router = APIRouter(prefix="/items", tags=["items"])

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[items.Item])
def get_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_items(db, skip=skip, limit=limit)

@router.post("/", response_model=items.Item)
def add_item(item: items.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item=item)
