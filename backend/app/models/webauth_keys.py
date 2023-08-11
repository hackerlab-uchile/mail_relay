from .users import User
from core.database import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

class WebauthKey(Base):
    __tablename__ = "webauthn_keys"

    #id = Column(CHAR(36), primary_key=True)
    id: Mapped[int] = mapped_column(primary_key=True)
    #user_id = Column(CHAR(36), ForeignKey(User.id, ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
    #credentialId = Column(String(255), index=True)
    credentialId: Mapped[str] = mapped_column(String(255), index=True)
    #type = Column(String(255))
    type: Mapped[str] = mapped_column(String(255))
