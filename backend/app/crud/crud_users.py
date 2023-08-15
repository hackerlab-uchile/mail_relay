from sqlalchemy.orm import Session
from app.models.users import UserBase, User

def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_all_users(db: Session):
    users = db.query(User).all()
    return {"users": users}