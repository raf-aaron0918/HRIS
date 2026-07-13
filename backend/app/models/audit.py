from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    module: Mapped[str] = mapped_column(String(80), index=True)
    action: Mapped[str] = mapped_column(String(80), index=True)
    record_id: Mapped[str] = mapped_column(String(80), index=True)
    actor: Mapped[str] = mapped_column(String(160))
    actor_role: Mapped[str] = mapped_column(String(80), nullable=True)
    summary: Mapped[str] = mapped_column(String(500), nullable=True)
    created_at: Mapped[str] = mapped_column(String(40), index=True)
