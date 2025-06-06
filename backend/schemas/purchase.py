from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List
from backend.schemas.store_product import StoreProductOut


class PurchaseItemCreate(BaseModel):
    product_id: int
    quantity: int


class PurchaseCreate(BaseModel):
    items: List[PurchaseItemCreate]


class PurchaseItemOut(BaseModel):
    product_id: int
    product: StoreProductOut
    quantity: int
    model_config = ConfigDict(from_attributes=True)


class PurchaseOut(BaseModel):
    id: int
    family_id: int
    purchased_at: datetime
    items: List[PurchaseItemOut]
    model_config = ConfigDict(from_attributes=True)
