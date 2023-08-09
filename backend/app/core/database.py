from databases import Database
from sqlalchemy import create_engine, MetaData

from .config import DATABASE_URL

metadata = MetaData()

# Databases query builder
database = Database(DATABASE_URL)

# SQLAlchemy specific
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)