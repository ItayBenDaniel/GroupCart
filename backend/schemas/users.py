from pydantic import BaseModel,EmailStr
from typing import Optional


# Schema for User, Extends the base model, adding username and email common to all users.
class UserBase(BaseModel):
    username: str
    email: EmailStr
# Schema for creating a user, Extends the UserBase model, adding password for user creation.
class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):  # ✅ new
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
# Schema for returning user data , passwords should not be returned in api requests.
class User(UserBase):
    id: int
    is_active: bool

    # Allows conversion of sqlalchemy objects to pydantic models.
    model_config = {
        "from_attributes": True  # this replaces `orm_mode = True`
    }