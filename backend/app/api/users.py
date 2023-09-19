from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.users import User, UserBase, UserCreate
from app.crud import crud_users
from app.core.security import get_password_hash, verify_password, create_access_token, get_current_user


router = APIRouter()


@router.post("/signup/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if crud_users.get_user_by_username(db, username=user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    if crud_users.get_user_by_recipient_email(db, recipient_email=user.recipient_email):
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = User(username=user.username, password=get_password_hash(user.password), recipient_email=user.recipient_email)
    return crud_users.create_user(db=db, user=db_user)


@router.post("/signin/")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud_users.get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me/")
def get_user_profile(current_user: User = Depends(get_current_user)):
    return current_user