from .users import User
from core.database import Base
from sqlalchemy import ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

class Alias(Base):
    __tablename__ = "aliases"

    #id = Column(CHAR(36), primary_key=True)
    id: Mapped[int] = mapped_column(primary_key=True)
    #user_id = Column(CHAR(36), ForeignKey(User.id, ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
    #email = Column(String(255), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    #active = Column(Boolean, default=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
