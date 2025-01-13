from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    quantity: int

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    purchased: bool

    class Config:
        orm_mode = True