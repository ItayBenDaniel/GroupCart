from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    quantity: int

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    purchased: bool

    class Config:
        orm_mode = True