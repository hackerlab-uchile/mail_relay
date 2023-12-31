from app.core.database import Base
from sqlalchemy import ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from pydantic import BaseModel


class Alias(Base):
    __tablename__ = "aliases"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)


# PYDANTIC
class AliasBase(BaseModel):
    active: Optional[bool] = True
    description: Optional[str] = None


class AliasUpdate(AliasBase):
    active: Optional[bool] = None
    description: Optional[str] = None
