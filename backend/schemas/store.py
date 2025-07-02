from pydantic import BaseModel, ConfigDict
from typing import Optional


class StoreBase(BaseModel):
    store_id: int
    chain_id: str
    subchain_id: str
    chain_name: str
    name: str
    address: Optional[str] = ""
    city: Optional[str] = ""
    latitude: Optional[str] = ""
    longitude: Optional[str] = ""
    zip_code: Optional[str] = ""


class StoreCreate(StoreBase):
    pass


class Store(StoreBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class StoreNearby(BaseModel):
    id: int
    name: str
    address: str
    latitude: str
    longitude: str
    distance_km: float
