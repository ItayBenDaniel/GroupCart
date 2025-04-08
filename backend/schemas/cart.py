from pydantic import BaseModel, ConfigDict
from typing import Optional


class CartBase(BaseModel):
    product_id: int
    quantity: int


class CartItemCreate(CartBase):
    pass


class CartItemUpdate(BaseModel):
    quantity: Optional[int] = None
    purchased: Optional[bool] = None


class CartItem(CartBase):
    id: int
    user_id: int
    purchased: bool
    model_config = ConfigDict(from_attributes=True)
