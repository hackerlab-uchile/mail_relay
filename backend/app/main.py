from fastapi import FastAPI
from app.core.database import Base, engine
from app.api import users, aliases

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(aliases.router, prefix="/aliases", tags=["aliases"])

@app.get("/")
def read_root():
    return {"Hello": "World"}
