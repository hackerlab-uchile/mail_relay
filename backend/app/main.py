from fastapi import FastAPI
from app.core.database import Base, engine
from app.api import users

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])

@app.get("/")
def read_root():
    return {"Hello": "World"}
