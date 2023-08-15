from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.users import User, UserBase
from app.crud import crud_users


router = APIRouter()


@router.post("/")
def create_user(user: UserBase, db: Session = Depends(get_db)):
    if crud_users.get_user_by_username(db, username=user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = User(username=user.username, password=user.password, remember_token=user.remember_token, recipient_email=user.recipient_email)
    return crud_users.create_user(db=db, user=db_user)

@router.get("/all/")
def read_user(db: Session = Depends(get_db)):
    db_user = crud_users.get_all_users(db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Users not found")
    return db_user
