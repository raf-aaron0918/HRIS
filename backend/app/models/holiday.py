from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Holiday(Base):
    __tablename__ = "holidays"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    holiday_id: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(160))
    holiday_date: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    holiday_type: Mapped[str] = mapped_column(String(40), default="Regular Holiday")
    notes: Mapped[str] = mapped_column(String(500), nullable=True)
