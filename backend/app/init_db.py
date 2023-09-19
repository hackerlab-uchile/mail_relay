from app.core.database import engine, Base, test_engine
from app.models.users import User
from app.models.aliases import Alias
#from app.models.webauth_keys import WebauthKey

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=test_engine)