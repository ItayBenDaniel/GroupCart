# models/family.py
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from backend.database import Base


class LikedItem(Base):
    __tablename__ = "liked_items"

    id = Column(Integer, primary_key=True, index=True)
    store_product_id = Column(Integer, ForeignKey("store_products.id"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    __table_args__ = (
        UniqueConstraint("user_id", "store_product_id", name="uq_user_item"),
    )
