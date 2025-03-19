from sqlalchemy.orm import Session
from backend.models.items import Item  # ✅ Correct Import
from backend.schemas.items import ItemCreate  # ✅ Schema import for validation

def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Item).offset(skip).limit(limit).all()

def create_item(db: Session, item: ItemCreate):
    db_item = Item(name=item.name, quantity=item.quantity, purchased=False)  # ✅ Using models.Item
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item