from sqlalchemy.orm import Session
from backend.schemas import items
from models import items

def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(items.Item).offset(skip).limit(limit).all()

def create_item(db: Session, item: items.ItemCreate):
    db_item = items.Item(name=item.name, quantity=item.quantity, purchased=False)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item