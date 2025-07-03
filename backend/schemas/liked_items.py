from pydantic import BaseModel


class LikedItemBase(BaseModel):
    store_product_id: int


class LikedItemCreate(LikedItemBase):
    pass
