from pydantic import BaseModel
from typing import Optional
class CartBase(BaseModel):
    product_id: int
    quantity: int

class CartItemCreate(CartBase):
    pass

class CartItemUpdate(CartBase):
    quantity: Optional[int] = None
    purchased: Optional[bool] = None
    
    
class CartItem(CartBase):
    id: int
    user_id: int
    purchased: bool
    model_config = {
        "from_attributes": True  
    }