from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class PromotionBase(BaseModel):
    promotion_id: str
    description: Optional[str] = ""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_coupon: bool = False
    is_member_exclusive: bool = False
    min_quantity: int = 1
    max_quantity: Optional[int] = None
    discount_type: Optional[str] = None
    discount_value: Optional[float] = None
    original_price: Optional[float] = None
    chain_id: str
    subchain_id: str
    store_id: Optional[int] = None


class PromotionCreate(PromotionBase):
    pass


class Promotion(PromotionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
