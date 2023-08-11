from core.database import Base
from sqlalchemy.orm import Mapped, mapped_column 
from sqlalchemy import String

class User(Base):
    __tablename__ = "users"

    #id = Column(CHAR(36), primary_key=True, index=True)
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    #username = Column(CHAR(36), unique=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    #password = Column(String(255))
    password: Mapped[str] = mapped_column(String(255))
    #remember_token = Column(String(100))
    remember_token: Mapped[str] = mapped_column(String(100))
    #recipient_email = Column(String(255), unique=True, index=True)
    recipient_email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
