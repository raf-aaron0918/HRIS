from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.schemas.payroll import PayrollCreate, PayrollListResponse, PayrollResponse, PayrollUpdate
from app.services.payroll import create_payroll_run, get_payroll_run_by_id, list_payroll_runs, update_payroll_run

router = APIRouter()


@router.get("", response_model=PayrollListResponse)
def get_payroll_runs(
    _: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> PayrollListResponse:
    runs = list_payroll_runs(db)
    return PayrollListResponse(items=runs, total=len(runs))


@router.post("", response_model=PayrollResponse, status_code=status.HTTP_201_CREATED)
def create_payroll_record(
    payload: PayrollCreate,
    _: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> PayrollResponse:
    if get_payroll_run_by_id(db, payload.payroll_run_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Payroll run ID already exists")

    record = create_payroll_run(db, payload.model_dump())
    return PayrollResponse.model_validate(record)


@router.put("/{payroll_run_id}", response_model=PayrollResponse)
def update_payroll_record(
    payroll_run_id: str,
    payload: PayrollUpdate,
    _: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> PayrollResponse:
    record = get_payroll_run_by_id(db, payroll_run_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payroll run not found")

    updated_record = update_payroll_run(db, record, payload.model_dump())
    return PayrollResponse.model_validate(updated_record)


@router.get("/summary")
def get_payroll_summary(
    _: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> dict:
    runs = list_payroll_runs(db)
    published_runs = [run for run in runs if run.payslip_status.lower() == "published"]

    return {
        "total_runs": len(runs),
        "published_runs": len(published_runs),
        "gross_pay_total": sum(run.gross_pay for run in runs),
        "deductions_total": sum(run.total_deductions for run in runs),
        "net_pay_total": sum(run.net_pay for run in runs),
        "recent_runs": [
            {
                "payroll_run_id": run.payroll_run_id,
                "employee_code": run.employee_code,
                "employee_name": run.employee_name,
                "cutoff": f"{run.cutoff_start} to {run.cutoff_end}",
                "net_pay": run.net_pay,
                "payslip_status": run.payslip_status,
            }
            for run in runs[:5]
        ],
    }
