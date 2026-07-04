from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class AttendanceLog(Base):
    __tablename__ = "attendance_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    log_id: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    employee_code: Mapped[str] = mapped_column(String(20), index=True)
    employee_name: Mapped[str] = mapped_column(String(160))
    work_date: Mapped[str] = mapped_column(String(20), index=True)
    shift_schedule: Mapped[str] = mapped_column(String(80), default="regular")
    shift_start: Mapped[str] = mapped_column(String(10))
    shift_end: Mapped[str] = mapped_column(String(10))
    clock_in: Mapped[str] = mapped_column(String(10))
    clock_out: Mapped[str] = mapped_column(String(10))
    source: Mapped[str] = mapped_column(String(50))
    break_out: Mapped[str] = mapped_column(String(10), nullable=True)
    break_in: Mapped[str] = mapped_column(String(10), nullable=True)
    log_action: Mapped[str] = mapped_column(String(40), default="original")
    rest_day_work: Mapped[str] = mapped_column(String(10), default="no")
    holiday_work: Mapped[str] = mapped_column(String(10), default="no")
    correction_type: Mapped[str] = mapped_column(String(80), nullable=True)
    adjustment_reason: Mapped[str] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="Draft")
    payable_hours: Mapped[float] = mapped_column(Float, default=0)
    notes: Mapped[str] = mapped_column(String(500), nullable=True)
