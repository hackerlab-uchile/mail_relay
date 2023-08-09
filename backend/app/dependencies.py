from databases import Database
from app.core.database import database

async def get_db():
    await database.connect()
    try:
        yield database
    finally:
        await database.disconnect()