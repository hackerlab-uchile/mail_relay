from app.core.database import engine, Base
from app.models.users import User
from app.models.aliases import Alias
from app.models.webauth_keys import WebauthKey

print("Creating database tables...")
Base.metadata.create_all(bind=engine)