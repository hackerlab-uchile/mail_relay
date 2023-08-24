from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import DATABASE_URL, TESTING, TEST_DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)
test_engine = create_engine(TEST_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(engine)
TestSessionLocal = sessionmaker(test_engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_test_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

class Base(DeclarativeBase):
    pass
