from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    employee_code: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(80))
    middle_name: Mapped[str] = mapped_column(String(80), nullable=True)
    last_name: Mapped[str] = mapped_column(String(80))
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    contact_number: Mapped[str] = mapped_column(String(40), nullable=True)
    birth_date: Mapped[str] = mapped_column(String(20), nullable=True)
    address: Mapped[str] = mapped_column(String(255), nullable=True)
    date_hired: Mapped[str] = mapped_column(String(20), nullable=True)
    department: Mapped[str] = mapped_column(String(120))
    position: Mapped[str] = mapped_column(String(120))
    branch: Mapped[str] = mapped_column(String(120), nullable=True)
    manager: Mapped[str] = mapped_column(String(120), nullable=True)
    pay_type: Mapped[str] = mapped_column(String(40), default="monthly")
    base_rate: Mapped[float] = mapped_column(Float, default=0)
    fixed_allowance: Mapped[float] = mapped_column(Float, default=0)
    work_schedule: Mapped[str] = mapped_column(String(80), default="regular")
    work_days: Mapped[str] = mapped_column(String(80), default="mon,tue,wed,thu,fri")
    default_shift_start: Mapped[str] = mapped_column(String(10), default="09:00")
    default_shift_end: Mapped[str] = mapped_column(String(10), default="18:00")
    default_grace_minutes: Mapped[int] = mapped_column(Integer, default=0)
    employment_status: Mapped[str] = mapped_column(String(50))
    account_status: Mapped[str] = mapped_column(String(50), nullable=True)
    onboarding_stage: Mapped[str] = mapped_column(String(50), nullable=True)
    movement_type: Mapped[str] = mapped_column(String(50), nullable=True)
    movement_effective_date: Mapped[str] = mapped_column(String(20), nullable=True)
    movement_remarks: Mapped[str] = mapped_column(String(255), nullable=True)
    offboarding_date: Mapped[str] = mapped_column(String(20), nullable=True)
    offboarding_reason: Mapped[str] = mapped_column(String(120), nullable=True)
    sss: Mapped[str] = mapped_column(String(20), nullable=True)
    philhealth: Mapped[str] = mapped_column(String(30), nullable=True)
    pagibig: Mapped[str] = mapped_column(String(20), nullable=True)
    tin: Mapped[str] = mapped_column(String(20), nullable=True)
    bank_account: Mapped[str] = mapped_column(String(255), nullable=True)
    emergency_contact: Mapped[str] = mapped_column(String(255), nullable=True)
    notes: Mapped[str] = mapped_column(String(500), nullable=True)
