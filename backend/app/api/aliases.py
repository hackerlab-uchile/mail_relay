from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.aliases import AliasBase, Alias
from app.crud import crud_aliases

router = APIRouter()

@router.post("/")
def create_alias(alias: AliasBase, db: Session = Depends(get_db)): 
    if crud_aliases.get_alias_by_email(db, email=alias.email):
        raise HTTPException(status_code=400, detail="Alias already registered")
    db_alias = Alias(user_id=alias.user_id, email=alias.email, active=alias.active)
    return crud_aliases.create_alias(db=db, alias=db_alias)

@router.get("/user/{user_id}")
def get_aliases_for_user(user_id: int, db: Session = Depends(get_db)):
    return crud_aliases.get_aliases_by_user_id(db, user_id)

@router.get("/all/")
def get_all_aliases(db: Session = Depends(get_db)):
    db_aliases = crud_aliases.get_all_aliases(db)
    if db_aliases is None:
        raise HTTPException(status_code=404, detail="Aliases not found")
    return db_aliases
