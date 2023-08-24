from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column 
from sqlalchemy import String
from pydantic import BaseModel

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))
    remember_token: Mapped[str] = mapped_column(String(100))
    recipient_email: Mapped[str] = mapped_column(String(255), unique=True, index=True)

#PYDANTIC
class UserBase(BaseModel):
    username: str
    recipient_email: str

class UserCreate(UserBase):
    password: str
    remember_token: str