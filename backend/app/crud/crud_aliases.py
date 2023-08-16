from sqlalchemy.orm import Session
from app.models.aliases import Alias

def create_alias(db: Session, alias: Alias):
    db.add(alias)
    db.commit()
    db.refresh(alias)
    return alias

def get_aliases_by_user_id(db: Session, user_id: int):
    return db.query(Alias).filter(Alias.user_id == user_id).all()

def get_alias_by_email(db: Session, email: str):
    return db.query(Alias).filter(Alias.email == email).first()

def get_all_aliases(db: Session):
    aliases = db.query(Alias).all()
    return {"aliases": aliases}