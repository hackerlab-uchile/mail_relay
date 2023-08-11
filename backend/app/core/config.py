import os

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@db/postgres")