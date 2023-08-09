from sqlalchemy import Table, Column, String, CHAR, ForeignKey, PrimaryKeyConstraint
from core.database import metadata

webauthn_keys = Table(
    "webauthn_keys",
    metadata,
    Column("id", CHAR(36), primary_key=True),
    Column("user_id", CHAR(36), ForeignKey("users.id", ondelete="CASCADE")),
    Column("credentialId", String(255), index=True),
    Column("type", String(255))
)