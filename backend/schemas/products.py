from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str
    description: str
    category: str
    price: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
