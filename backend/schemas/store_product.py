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
    quantity_in_package: Optional[str] = ""
    price: Optional[float] = None
    discounted: bool = False


class StoreProductCreate(StoreProductBase):
    pass


class StoreProduct(StoreProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
