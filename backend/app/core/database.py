from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)

class Base(DeclarativeBase):
    pass
