from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.aliases import AliasBase, Alias
from app.models.users import User
from app.core.security import get_current_user
from app.crud import crud_aliases

router = APIRouter()

@router.post("/")
def create_alias(alias: AliasBase, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if crud_aliases.get_alias_by_email(db, email=alias.email):
        raise HTTPException(status_code=400, detail="Alias already registered")
    db_alias = Alias(user_id=current_user.id, email=alias.email, active=alias.active)
    return crud_aliases.create_alias(db=db, alias=db_alias)

@router.get("/")
def get_aliases_for_user(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_aliases = crud_aliases.get_aliases_by_user_id(db, current_user.id)
    if not user_aliases:
        raise HTTPException(status_code=404, detail="No aliases found for this user.")
    return user_aliases

@router.get("/{alias_id}")
def get_specific_alias(alias_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_alias = crud_aliases.get_alias_by_id(db, alias_id)
    if not db_alias:
        raise HTTPException(status_code=404, detail="Alias not found.")
    if db_alias.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this alias.")
    return db_alias

@router.put("/{alias_id}")
def update_specific_alias(alias: AliasBase, alias_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_alias = crud_aliases.get_alias_by_id(db, alias_id)
    if not db_alias:
        raise HTTPException(status_code=404, detail="Alias not found.")
    if db_alias.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this alias.")
    return crud_aliases.update_alias(db=db, alias_id=alias_id, alias_update_data=alias)

@router.delete("/{alias_id}")
def delete_specific_alias(alias_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_alias = crud_aliases.get_alias_by_id(db, alias_id)
    if not db_alias:
        raise HTTPException(status_code=404, detail="Alias not found.")
    if db_alias.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this alias.")
    return crud_aliases.delete_alias(db=db, alias_id=alias_id)
