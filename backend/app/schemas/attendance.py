from pydantic import BaseModel, ConfigDict, Field


class AttendanceBase(BaseModel):
    log_id: str
    employee_code: str
    employee_name: str
    work_date: str
    shift_schedule: str = "regular"
    shift_start: str
    shift_end: str
    grace_minutes: int = Field(default=0, ge=0, le=120)
    clock_in: str
    clock_out: str
    source: str = "HRIS"
    break_out: str | None = None
    break_in: str | None = None
    log_action: str = "original"
    rest_day_work: str = "no"
    holiday_work: str = "no"
    correction_type: str | None = None
    adjustment_reason: str | None = None
    status: str = "Draft"
    worked_hours: float = 0
    payable_hours: float = 0
    late_minutes: int = 0
    undertime_minutes: int = 0
    overtime_minutes: int = 0
    night_diff_minutes: int = 0
    notes: str | None = None


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceUpdate(BaseModel):
    employee_code: str
    employee_name: str
    work_date: str
    shift_schedule: str = "regular"
    shift_start: str
    shift_end: str
    grace_minutes: int = Field(default=0, ge=0, le=120)
    clock_in: str
    clock_out: str
    source: str = "HRIS"
    break_out: str | None = None
    break_in: str | None = None
    log_action: str = "original"
    rest_day_work: str = "no"
    holiday_work: str = "no"
    correction_type: str | None = None
    adjustment_reason: str | None = None
    status: str = "Draft"
    worked_hours: float = 0
    payable_hours: float = 0
    late_minutes: int = 0
    undertime_minutes: int = 0
    overtime_minutes: int = 0
    night_diff_minutes: int = 0
    notes: str | None = None


class AttendanceResponse(AttendanceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class AttendanceListResponse(BaseModel):
    items: list[AttendanceResponse]
    total: int
