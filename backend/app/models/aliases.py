from sqlalchemy import Table, Column, String, CHAR, Boolean, ForeignKey, PrimaryKeyConstraint
from core.database import metadata

aliases = Table(
    "aliases",
    metadata,
    Column("id", CHAR(36), primary_key=True),
    Column("user_id", CHAR(36), ForeignKey("users.id", ondelete="CASCADE")),
    Column("email", String(255), unique=True),
    Column("active", Boolean, default=True)
)