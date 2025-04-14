from sqlalchemy import Column, Integer, Boolean, ForeignKey
from backend.database import Base
from sqlalchemy.orm import relationship


class CartDB(Base):
    __tablename__ = "shopping_cart"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    family_id = Column(
        Integer, ForeignKey("families.id"), nullable=False
    )  # which family the cart belongs to
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)
    purchased = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)

    user = relationship("User", back_populates="cart_items")
    family = relationship("Family", back_populates="cart_items")
    product = relationship("Product")
