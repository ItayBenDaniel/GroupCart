from sqlalchemy import Column, Integer, String, Boolean
from backend.database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Integer)
    purchased = Column(Boolean, default=False)