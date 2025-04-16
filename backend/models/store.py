from sqlalchemy import Column, Integer, String
from backend.database import Base


class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, index=True)
    chain_id = Column(String, index=True)
    chain_name = Column(String, default="")
    name = Column(String)
    address = Column(String, default="")
    city = Column(String, default="")
    latitude = Column(String, default="", nullable=True)
    longitude = Column(String, default="", nullable=True)
