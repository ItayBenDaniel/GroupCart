from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    description: str
    category: str
    price: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    model_config = {
        "from_attributes": True  # this replaces `orm_mode = True`
    }