from pydantic import BaseModel, ConfigDict


class PayrollBase(BaseModel):
    payroll_run_id: str
    cutoff_start: str
    cutoff_end: str
    payroll_mode: str = "regular"
    payslip_status: str = "Draft"
    employee_code: str
    employee_name: str
    department: str | None = None
    position: str | None = None
    branch: str | None = None
    base_pay: float = 0
    ot_pay: float = 0
    holiday_pay: float = 0
    night_diff_pay: float = 0
    allowances: float = 0
    tax_deduction: float = 0
    sss_deduction: float = 0
    philhealth_deduction: float = 0
    pagibig_deduction: float = 0
    gross_pay: float = 0
    total_deductions: float = 0
    net_pay: float = 0
    remarks: str | None = None


class PayrollCreate(PayrollBase):
    pass


class PayrollUpdate(BaseModel):
    cutoff_start: str
    cutoff_end: str
    payroll_mode: str = "regular"
    payslip_status: str = "Draft"
    employee_code: str
    employee_name: str
    department: str | None = None
    position: str | None = None
    branch: str | None = None
    base_pay: float = 0
    ot_pay: float = 0
    holiday_pay: float = 0
    night_diff_pay: float = 0
    allowances: float = 0
    tax_deduction: float = 0
    sss_deduction: float = 0
    philhealth_deduction: float = 0
    pagibig_deduction: float = 0
    gross_pay: float = 0
    total_deductions: float = 0
    net_pay: float = 0
    remarks: str | None = None


class PayrollResponse(PayrollBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class PayrollListResponse(BaseModel):
    items: list[PayrollResponse]
    total: int
