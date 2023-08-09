from sqlalchemy import Table, Column, String, CHAR
from core.database import metadata

users = Table(
    "users",
    metadata,
    Column("id", CHAR(36), primary_key=True, index=True),
    Column("username", CHAR(36), unique=True, index=True),
    Column("password", String(255)),
    Column("remember_token", String(100)),
    Column("recipient_email", String(255), unique=True, index=True),
)