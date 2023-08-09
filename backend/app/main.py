from fastapi import FastAPI, Depends
from app.models import users
from app.dependencies import get_db
from databases import Database

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/users/")
async def read_users(db: Database = Depends(get_db)):
    query = users.select()
    return await db.fetch_all(query)

'''from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}'''