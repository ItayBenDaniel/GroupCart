from sqlalchemy import Column, Integer, String, Boolean
from backend.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, default="")
    category = Column(String, default="Miscellaneous")
    price = Column(Integer)