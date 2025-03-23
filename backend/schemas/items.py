from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    quantity: int

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    purchased: bool

    model_config = {
        "from_attributes": True  # this replaces `orm_mode = True`
    }