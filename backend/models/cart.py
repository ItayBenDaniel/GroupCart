from sqlalchemy import Column, Integer, Boolean,ForeignKey
from backend.database import Base


class CartDB(Base):
    __tablename__ = "shopping_cart"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)
    purchased = Column(Boolean, default=False)