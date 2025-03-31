from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models.users import User
from backend.core.utils import (
    verify_password,
    create_jwt_token,
    hash_password,
    get_current_user,
)
from backend.schemas import users as schemas
from backend.crud import users as crud
from backend import database


router = APIRouter(prefix="/users", tags=["users"])


# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/signup", response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(crud.User).filter(crud.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)


@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # Generate JWT token
    access_token = create_jwt_token(db_user.id)
    return {"access_token": access_token, "token_type": "bearer"}


@router.patch("/update", response_model=schemas.User)
def update_user_me(
    update_data: schemas.UserUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    # Get the user from the database
    user = db.query(User).filter(User.id == user_id).first()
    # If the user is not found, raise an HTTPException
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Only update fields that are provided
    if update_data.username:
        user.username = update_data.username
    if update_data.email:
        user.email = update_data.email
    if update_data.password:
        user.hashed_password = hash_password(update_data.password)

    # Commit the changes to the database
    db.commit()
    db.refresh(user)
    return user
