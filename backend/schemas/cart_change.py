from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CartChangeBase(BaseModel):
    action: str
    store_product_id: int
    name: Optional[str] = None
    quantity: Optional[int] = None
    previous_quantity: Optional[int] = None


class CartChangeCreate(CartChangeBase):
    family_id: int
    username: str


class CartChangeOut(CartChangeBase):
    id: int
    family_id: int
    username: str
    timestamp: datetime
    undone: int

    class Config:
        from_attributes = True
