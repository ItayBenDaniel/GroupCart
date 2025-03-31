from pydantic import BaseModel
from datetime import datetime
from typing import List


class PurchaseItemCreate(BaseModel):
    product_id: int
    quantity: int


class PurchaseCreate(BaseModel):
    items: List[PurchaseItemCreate]


class PurchaseItemOut(BaseModel):
    product_id: int
    quantity: int

    class Config:
        orm_mode = True


class PurchaseOut(BaseModel):
    id: int
    user_id: int
    purchased_at: datetime
    items: List[PurchaseItemOut]

    class Config:
        orm_mode = True
