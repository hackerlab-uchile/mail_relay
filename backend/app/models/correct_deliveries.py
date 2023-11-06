from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column, Integer, DateTime, String
from app.core.database import Base
import datetime


class CorrectDelivery(Base):
    __tablename__ = "correct_deliveries"

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )
    from_address: Mapped[str] = mapped_column(String)
    to_address: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)
