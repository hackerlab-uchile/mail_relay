from fastapi import FastAPI
from .core.database import Base, engine

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
