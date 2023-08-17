from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.users import User, UserBase
from app.crud import crud_users
from app.core.security import get_password_hash, verify_password, create_access_token, get_current_user


router = APIRouter()


@router.post("/")
def create_user(user: UserBase, db: Session = Depends(get_db)):
    if crud_users.get_user_by_username(db, username=user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = User(username=user.username, password=get_password_hash(user.password), remember_token=user.remember_token, recipient_email=user.recipient_email)
    return crud_users.create_user(db=db, user=db_user)

@router.get("/all/")
def read_user(db: Session = Depends(get_db)):
    db_user = crud_users.get_all_users(db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Users not found")
    return db_user


@router.post("/token/")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud_users.get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me/")
def get_user_profile(current_user: User = Depends(get_current_user)):
    return current_user