from pydantic import BaseModel
from typing import Optional


class FamilyBase(BaseModel):
    name: str


class FamilyCreate(FamilyBase):
    pass


class FamilyOut(FamilyBase):
    id: int
    owner_id: int

    model_config = {"from_attributes": True}
