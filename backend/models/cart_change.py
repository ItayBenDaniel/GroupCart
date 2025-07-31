from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class CartChange(Base):
    __tablename__ = "cart_changes"

    id = Column(Integer, primary_key=True)
    family_id = Column(Integer, ForeignKey("families.id"))
    username = Column(String)
    action = Column(String)
    store_product_id = Column(Integer)
    name = Column(String)
    quantity = Column(Integer)
    undone = Column(Integer, nullable=True)
    previous_quantity = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
