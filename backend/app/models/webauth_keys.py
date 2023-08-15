#from .users import User
#from core.database import Base
##from app.models.users import User
from app.core.database import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

class WebauthKey(Base):
    __tablename__ = "webauthn_keys"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    credentialId: Mapped[str] = mapped_column(String(255), index=True)
    type: Mapped[str] = mapped_column(String(255))

#PYDANTIC
class WebauthKeyBase(Base):
    credentialId: str
    type: str