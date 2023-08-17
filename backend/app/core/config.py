import os

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@db/postgres")
SECRET_KEY = os.environ.get("SECRET_KEY","09d25e094faa6ca2556c818166b7a3182b93f7099f6f0f4caz6cf63b88e8d3e7") # openssl rand -hex 32
ALGORITHM = os.environ.get("ALGORITHM","HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 20)