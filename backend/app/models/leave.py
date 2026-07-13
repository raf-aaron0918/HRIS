from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    request_id: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    employee_name: Mapped[str] = mapped_column(String(160), index=True)
    leave_type: Mapped[str] = mapped_column(String(50), index=True)
    start_date: Mapped[str] = mapped_column(String(20))
    end_date: Mapped[str] = mapped_column(String(20))
    leave_mode: Mapped[str] = mapped_column(String(30), default="full")
    reason: Mapped[str] = mapped_column(String(500))
    attachment_name: Mapped[str] = mapped_column(String(255), nullable=True)
    attachment_data_url: Mapped[str] = mapped_column(String, nullable=True)
    attachment_mime_type: Mapped[str] = mapped_column(String(120), nullable=True)
    approver: Mapped[str] = mapped_column(String(160))
    status: Mapped[str] = mapped_column(String(50), default="Draft", index=True)
    leave_days: Mapped[float] = mapped_column(Float, default=0)
    credits_used: Mapped[float] = mapped_column(Float, default=0)
    payroll_impact: Mapped[float] = mapped_column(Float, default=0)
    notes: Mapped[str] = mapped_column(String(500), nullable=True)
    updated_at: Mapped[str] = mapped_column(String(40), index=True, default="")
