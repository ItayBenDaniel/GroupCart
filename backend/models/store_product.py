from sqlalchemy import Column, Integer, String, Boolean, Float
from backend.database import Base


class StoreProduct(Base):
    __tablename__ = "store_products"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, index=True)
    item_code = Column(String, index=True)
    name = Column(String)
    manufacturer_name = Column(String, default="")
    manufacturer_country = Column(String, default="")
    item_description = Column(String, default="")
    unit_quantity = Column(String, default="")
    quantity_in_package = Column(Integer, default="", nullable=True)
    price = Column(Float, nullable=True)
    discounted = Column(Boolean, default=False)
