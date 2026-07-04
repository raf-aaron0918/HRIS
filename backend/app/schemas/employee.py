from pydantic import BaseModel, ConfigDict, EmailStr


class EmployeeBase(BaseModel):
    employee_code: str
    first_name: str
    middle_name: str | None = None
    last_name: str
    email: str
    contact_number: str | None = None
    birth_date: str | None = None
    address: str | None = None
    date_hired: str | None = None
    department: str
    position: str
    branch: str | None = None
    manager: str | None = None
    employment_status: str
    account_status: str | None = None
    onboarding_stage: str | None = None
    movement_type: str | None = None
    movement_effective_date: str | None = None
    movement_remarks: str | None = None
    offboarding_date: str | None = None
    offboarding_reason: str | None = None
    sss: str | None = None
    philhealth: str | None = None
    pagibig: str | None = None
    tin: str | None = None
    bank_account: str | None = None
    emergency_contact: str | None = None
    notes: str | None = None


class EmployeeCreate(EmployeeBase):
    email: EmailStr


class EmployeeWrite(BaseModel):
    first_name: str
    middle_name: str | None = None
    last_name: str
    email: EmailStr
    contact_number: str | None = None
    birth_date: str | None = None
    address: str | None = None
    date_hired: str | None = None
    department: str
    position: str
    branch: str | None = None
    manager: str | None = None
    employment_status: str
    account_status: str | None = None
    onboarding_stage: str | None = None
    movement_type: str | None = None
    movement_effective_date: str | None = None
    movement_remarks: str | None = None
    offboarding_date: str | None = None
    offboarding_reason: str | None = None
    sss: str | None = None
    philhealth: str | None = None
    pagibig: str | None = None
    tin: str | None = None
    bank_account: str | None = None
    emergency_contact: str | None = None
    notes: str | None = None


class EmployeeUpdate(EmployeeWrite):
    pass


class EmployeeResponse(EmployeeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class EmployeeListResponse(BaseModel):
    items: list[EmployeeResponse]
    total: int
