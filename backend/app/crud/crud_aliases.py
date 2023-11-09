from sqlalchemy.orm import Session
from app.models.aliases import Alias, AliasUpdate
from random import choice, randint
from sqlalchemy.exc import IntegrityError
from app.core.config import DOMAIN


def generate_random_alias():
    animals = ["lion", "tiger", "bear", "eagle", "shark"]
    adjectives = ["swift", "mighty", "brave", "sly", "quick"]
    number = randint(0, 999)
    return f"{choice(adjectives)}.{choice(animals)}.{number}@{DOMAIN}"


def create_alias(
    db: Session, user_id: int, active: bool = True, description: str = None
):
    attempts = 0
    while attempts < 5:
        unique_alias_email = generate_random_alias()
        new_alias = Alias(
            user_id=user_id,
            email=unique_alias_email,
            active=active,
            description=description,
        )
        try:
            db.add(new_alias)
            db.commit()
            db.refresh(new_alias)
            return new_alias
        except IntegrityError:
            db.rollback()
            attempts += 1

    raise Exception("Failed to generate a unique alias after several attempts.")


def get_aliases_by_user_id(db: Session, user_id: int):
    return (
        db.query(Alias).filter(Alias.user_id == user_id and not Alias.is_deleted).all()
    )


def get_alias_by_email(db: Session, email: str):
    return db.query(Alias).filter(Alias.email == email).first()


def get_all_aliases(db: Session):
    aliases = db.query(Alias).all()
    return {"aliases": aliases}


def get_alias_by_id(db: Session, alias_id: int):
    return db.query(Alias).filter(Alias.id == alias_id).first()


def update_alias(db: Session, alias_id: int, alias_update_data: AliasUpdate):
    db_alias = db.query(Alias).filter(Alias.id == alias_id).first()
    if alias_update_data.active != None:
        db_alias.active = alias_update_data.active
    if alias_update_data.description != None:
        db_alias.description = alias_update_data.description
    db.commit()
    db.refresh(db_alias)
    return db_alias


def delete_alias(db: Session, alias_id: int):
    db_alias = db.query(Alias).filter(Alias.id == alias_id).first()
    db_alias.is_deleted = True
    db.commit()
    return {"message": "Alias deleted."}
