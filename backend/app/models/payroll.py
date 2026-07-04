from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class PayrollRun(Base):
    __tablename__ = "payroll_runs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    payroll_run_id: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    cutoff_start: Mapped[str] = mapped_column(String(20))
    cutoff_end: Mapped[str] = mapped_column(String(20))
    payroll_mode: Mapped[str] = mapped_column(String(40), default="regular")
    payslip_status: Mapped[str] = mapped_column(String(40), default="Draft", index=True)
    employee_code: Mapped[str] = mapped_column(String(20), index=True)
    employee_name: Mapped[str] = mapped_column(String(160))
    department: Mapped[str] = mapped_column(String(120), nullable=True)
    position: Mapped[str] = mapped_column(String(120), nullable=True)
    branch: Mapped[str] = mapped_column(String(120), nullable=True)
    base_pay: Mapped[float] = mapped_column(Float, default=0)
    ot_pay: Mapped[float] = mapped_column(Float, default=0)
    holiday_pay: Mapped[float] = mapped_column(Float, default=0)
    night_diff_pay: Mapped[float] = mapped_column(Float, default=0)
    allowances: Mapped[float] = mapped_column(Float, default=0)
    tax_deduction: Mapped[float] = mapped_column(Float, default=0)
    sss_deduction: Mapped[float] = mapped_column(Float, default=0)
    philhealth_deduction: Mapped[float] = mapped_column(Float, default=0)
    pagibig_deduction: Mapped[float] = mapped_column(Float, default=0)
    gross_pay: Mapped[float] = mapped_column(Float, default=0)
    total_deductions: Mapped[float] = mapped_column(Float, default=0)
    net_pay: Mapped[float] = mapped_column(Float, default=0)
    remarks: Mapped[str] = mapped_column(String(500), nullable=True)
