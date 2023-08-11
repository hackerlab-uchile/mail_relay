from core.database import engine, Base
from models.users import User
from models.aliases import Alias
from models.webauth_keys import WebauthKey


print("Creating database tables...")
Base.metadata.create_all(bind=engine)