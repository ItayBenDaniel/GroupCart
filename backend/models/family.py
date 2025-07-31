# models/family.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base
from backend.models.users import User


class Family(Base):
    __tablename__ = "families"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", foreign_keys=[owner_id])
    cart_items = relationship("CartDB", back_populates="family")
    members = relationship(
        "User",
        back_populates="family",
        foreign_keys=[User.family_id],
    )
