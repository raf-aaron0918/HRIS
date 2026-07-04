from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.services.attendance import list_attendance_logs
from app.services.employee import list_employees
from app.services.leave import list_leave_requests
from app.services.payroll import list_payroll_runs

router = APIRouter()


@router.get("")
def get_reports(_: User = Depends(get_current_active_user)) -> dict:
    return {
        "available_reports": [
            "Employee Masterlist",
            "Attendance Report",
            "Leave Report",
            "Payroll Report",
            "Government Contribution Report",
        ]
    }


@router.get("/data")
def get_report_data(
    report_type: str = Query(default="employee"),
    _: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> dict:
    if report_type == "attendance":
        rows = [
            {
                "log_id": log.log_id,
                "employee_code": log.employee_code,
                "employee_name": log.employee_name,
                "work_date": log.work_date,
                "clock_in": log.clock_in,
                "clock_out": log.clock_out,
                "status": log.status,
                "payable_hours": log.payable_hours,
            }
            for log in list_attendance_logs(db)
        ]
        return {"report_type": report_type, "rows": rows, "total": len(rows)}

    if report_type == "leave":
        rows = [
            {
                "request_id": request.request_id,
                "employee_name": request.employee_name,
                "leave_type": request.leave_type,
                "start_date": request.start_date,
                "end_date": request.end_date,
                "status": request.status,
                "credits_used": request.credits_used,
            }
            for request in list_leave_requests(db)
        ]
        return {"report_type": report_type, "rows": rows, "total": len(rows)}

    if report_type == "payroll":
        rows = [
            {
                "payroll_run_id": run.payroll_run_id,
                "employee_code": run.employee_code,
                "employee_name": run.employee_name,
                "cutoff_start": run.cutoff_start,
                "cutoff_end": run.cutoff_end,
                "gross_pay": run.gross_pay,
                "total_deductions": run.total_deductions,
                "net_pay": run.net_pay,
                "payslip_status": run.payslip_status,
            }
            for run in list_payroll_runs(db)
        ]
        return {"report_type": report_type, "rows": rows, "total": len(rows)}

    rows = [
        {
            "employee_code": employee.employee_code,
            "employee_name": f"{employee.first_name} {employee.last_name}",
            "department": employee.department,
            "position": employee.position,
            "branch": employee.branch,
            "employment_status": employee.employment_status,
            "account_status": employee.account_status,
            "email": employee.email,
        }
        for employee in list_employees(db)
    ]
    return {"report_type": "employee", "rows": rows, "total": len(rows)}
