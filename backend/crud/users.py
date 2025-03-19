from sqlalchemy.orm import Session
from backend.models.users import User
from backend.schemas.users import UserCreate
from backend.core.utils import hash_password

def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user