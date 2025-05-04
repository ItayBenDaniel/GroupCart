from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from backend.database import Base


class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True)
    promotion_id = Column(String, unique=True, index=True)
    description = Column(String, default="")
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    is_coupon = Column(Boolean, default=False)
    is_member_exclusive = Column(Boolean, default=False)
    min_quantity = Column(Integer, default=1)
    max_quantity = Column(Integer, nullable=True)
    discount_type = Column(String)
    discount_value = Column(Float, nullable=True)
    original_price = Column(Float, nullable=True)
    chain_id = Column(String, index=True)
    subchain_id = Column(String, index=True)
    store_id = Column(Integer, index=True)
