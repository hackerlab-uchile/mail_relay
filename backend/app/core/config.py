import os

DATABASE_URL = os.environ.get("DATABASE_URL")
SECRET_KEY = os.environ.get("SECRET_KEY")  # openssl rand -hex 32
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
TESTING = bool(os.environ.get("TESTING"))
TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL")
CLOUDFLARE_SECRET_KEY = os.environ.get("CLOUDFLARE_SECRET_KEY")
