from pydantic import BaseModel, ConfigDict
from typing import Optional


class StoreProductBase(BaseModel):
    store_id: int
    item_code: str
    name: str
    manufacturer_name: Optional[str] = ""
    manufacturer_country: Optional[str] = ""
    item_description: Optional[str] = ""
    unit_quantity: Optional[str] = ""
    unit_of_measure: Optional[str] = ""
    quantity_in_package: Optional[str] = ""
    price: Optional[float] = None
    discounted: bool = False
    has_image: bool = False
    category: Optional[str] = ""
    promotion_price: Optional[float] = None


class StoreProductCreate(StoreProductBase):
    pass


class StoreProduct(StoreProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class StoreProductOut(BaseModel):
    id: int
    name: str
    item_code: str
    price: Optional[float]
    unit_of_measure: Optional[str]
    category: Optional[str]
    promotion_price: Optional[float] = None

    class Config:
        from_attributes = True
