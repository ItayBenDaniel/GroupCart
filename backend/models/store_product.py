from sqlalchemy import ForeignKey, Column, Integer, String, Boolean, Float
from backend.database import Base
from sqlalchemy.orm import relationship


class StoreProduct(Base):
    __tablename__ = "store_products"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"))
    item_code = Column(String, index=True)
    name = Column(String)
    category = Column(String, default="אחר")
    manufacturer_name = Column(String, default="")
    manufacturer_country = Column(String, default="")
    item_description = Column(String, default="")
    unit_of_measure = Column(String, default="")
    unit_quantity = Column(String, default="")
    quantity_in_package = Column(String, default="", nullable=True)
    price = Column(Float, nullable=True)
    discounted = Column(Boolean, default=False)
    has_image = Column(Boolean, default=False, index=True)
    promotion_price = Column(Float, nullable=True)
    store = relationship("Store")
