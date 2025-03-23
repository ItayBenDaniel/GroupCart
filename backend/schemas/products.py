from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    quantity: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    purchased: bool

    model_config = {
        "from_attributes": True  # this replaces `orm_mode = True`
    }