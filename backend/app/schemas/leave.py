from pydantic import BaseModel, ConfigDict


class LeaveBase(BaseModel):
    request_id: str
    employee_name: str
    leave_type: str
    start_date: str
    end_date: str
    leave_mode: str = "full"
    reason: str
    attachment_name: str | None = None
    attachment_data_url: str | None = None
    attachment_mime_type: str | None = None
    approver: str
    status: str = "Draft"
    leave_days: float = 0
    credits_used: float = 0
    payroll_impact: float = 0
    notes: str | None = None


class LeaveCreate(LeaveBase):
    pass


class LeaveUpdate(BaseModel):
    employee_name: str
    leave_type: str
    start_date: str
    end_date: str
    leave_mode: str = "full"
    reason: str
    attachment_name: str | None = None
    attachment_data_url: str | None = None
    attachment_mime_type: str | None = None
    approver: str
    status: str = "Draft"
    leave_days: float = 0
    credits_used: float = 0
    payroll_impact: float = 0
    notes: str | None = None


class LeaveResponse(LeaveBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    updated_at: str | None = None


class LeaveListResponse(BaseModel):
    items: list[LeaveResponse]
    total: int
