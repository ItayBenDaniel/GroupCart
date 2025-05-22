from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    purchased_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="purchases")
    items = relationship(
        "PurchaseItem", back_populates="purchase", cascade="all, delete-orphan"
    )


class PurchaseItem(Base):
    __tablename__ = "purchase_items"

    id = Column(Integer, primary_key=True, index=True)
    purchase_id = Column(Integer, ForeignKey("purchases.id"))
    product_id = Column(Integer, ForeignKey("store_products.id"))
    quantity = Column(Integer)

    purchase = relationship("Purchase", back_populates="items")
    product = relationship("StoreProduct")
