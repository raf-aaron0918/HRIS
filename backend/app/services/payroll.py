from sqlalchemy.orm import Session

from app.models.payroll import PayrollRun


def money(value: float) -> float:
    return round(float(value or 0), 2)


def calculate_pagibig_employee_share(monthly_basic_salary: float) -> float:
    salary = max(0, float(monthly_basic_salary or 0))
    salary_base = min(salary, 10000)
    rate = 0.01 if salary <= 1500 else 0.02
    return money(min(salary_base * rate, 200))


def calculate_philhealth_employee_share(monthly_basic_salary: float) -> float:
    salary = max(0, float(monthly_basic_salary or 0))
    if salary <= 0:
        return 0
    salary_base = min(max(salary, 10000), 100000)
    return money(salary_base * 0.025)


def calculate_sss_employee_share(monthly_basic_salary: float) -> float:
    salary = max(0, float(monthly_basic_salary or 0))
    if salary <= 0:
        return 0
    bounded_salary = min(max(salary, 5000), 35000)
    monthly_salary_credit = int((bounded_salary + 250) // 500) * 500
    monthly_salary_credit = min(max(monthly_salary_credit, 5000), 35000)
    return money(monthly_salary_credit * 0.05)


def calculate_statutory_deductions(monthly_basic_salary: float) -> dict[str, float]:
    return {
        "sss_deduction": calculate_sss_employee_share(monthly_basic_salary),
        "philhealth_deduction": calculate_philhealth_employee_share(monthly_basic_salary),
        "pagibig_deduction": calculate_pagibig_employee_share(monthly_basic_salary),
    }


def apply_payroll_calculations(payload: dict) -> dict:
    normalized_payload = dict(payload)
    base_pay = money(normalized_payload.get("base_pay", 0))
    normalized_payload.update(calculate_statutory_deductions(base_pay))

    gross_pay = money(
        base_pay
        + float(normalized_payload.get("ot_pay") or 0)
        + float(normalized_payload.get("holiday_pay") or 0)
        + float(normalized_payload.get("night_diff_pay") or 0)
        + float(normalized_payload.get("allowances") or 0)
    )
    total_deductions = money(
        float(normalized_payload.get("tax_deduction") or 0)
        + normalized_payload["sss_deduction"]
        + normalized_payload["philhealth_deduction"]
        + normalized_payload["pagibig_deduction"]
    )

    normalized_payload["base_pay"] = base_pay
    normalized_payload["gross_pay"] = gross_pay
    normalized_payload["total_deductions"] = total_deductions
    normalized_payload["net_pay"] = money(gross_pay - total_deductions)
    return normalized_payload


def list_payroll_runs(db: Session) -> list[PayrollRun]:
    return db.query(PayrollRun).order_by(PayrollRun.cutoff_end.desc(), PayrollRun.id.desc()).all()


def get_payroll_run_by_id(db: Session, payroll_run_id: str) -> PayrollRun | None:
    return db.query(PayrollRun).filter(PayrollRun.payroll_run_id == payroll_run_id).first()


def create_payroll_run(db: Session, payload: dict) -> PayrollRun:
    record = PayrollRun(**apply_payroll_calculations(payload))
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def update_payroll_run(db: Session, record: PayrollRun, payload: dict) -> PayrollRun:
    for field, value in apply_payroll_calculations(payload).items():
        setattr(record, field, value)

    db.add(record)
    db.commit()
    db.refresh(record)
    return record
