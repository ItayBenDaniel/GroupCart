from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from backend.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    purchases = relationship("Purchase", back_populates="user")
    family_id = Column(Integer, ForeignKey("families.id"), nullable=True)
    family = relationship("Family", back_populates="members", foreign_keys=[family_id])
