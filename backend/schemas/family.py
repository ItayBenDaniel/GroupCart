from pydantic import BaseModel
from typing import Optional, List


class FamilyBase(BaseModel):
    name: str


class FamilyCreate(FamilyBase):
    pass


class FamilyMember(BaseModel):
    id: int
    username: str
    email: str

    model_config = {"from_attributes": True}


class FamilyOut(FamilyBase):
    id: int
    owner_id: int
    members: List[FamilyMember]

    model_config = {"from_attributes": True}
