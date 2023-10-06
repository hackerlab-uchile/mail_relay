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


def get_alias_by_id(db: Session, alias_id: int):
    return db.query(Alias).filter(Alias.id == alias_id).first()


def update_alias(db: Session, alias_id: int, alias_update_data):
    db_alias = db.query(Alias).filter(Alias.id == alias_id).first()
    if alias_update_data.email:
        db_alias.email = alias_update_data.email
    if alias_update_data.active != None:
        db_alias.active = alias_update_data.active
    db.commit()
    db.refresh(db_alias)
    return db_alias


def delete_alias(db: Session, alias_id: int):
    db_alias = db.query(Alias).filter(Alias.id == alias_id).first()
    db.delete(db_alias)
    db.commit()
    return {"message": "Alias deleted."}
