from fastapi import FastAPI
from app.core.database import Base, engine
from app.api import users, aliases
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(aliases.router, prefix="/aliases", tags=["aliases"])


cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}
