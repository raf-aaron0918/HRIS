from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.schemas.attendance import AttendanceCreate, AttendanceListResponse, AttendanceResponse, AttendanceUpdate
from app.services.audit import create_audit_log
from app.services.attendance import (
    approved_leave_by_employee_name,
    create_attendance_log,
    find_duplicate_attendance_log,
    get_attendance_log_by_id,
    is_employee_scheduled_for_date,
    list_attendance_logs,
    normalize_employee_name,
    update_attendance_log,
)
from app.services.employee import list_employees
from app.services.holiday import get_holiday_by_date, list_holidays
from app.services.leave import list_leave_requests

router = APIRouter()


def scheduled_hours_for_employee(employee) -> float:
    start_parts = str(employee.default_shift_start or "09:00").split(":", maxsplit=1)
    end_parts = str(employee.default_shift_end or "18:00").split(":", maxsplit=1)
    try:
        start_minutes = int(start_parts[0]) * 60 + int(start_parts[1])
        end_minutes = int(end_parts[0]) * 60 + int(end_parts[1])
    except (IndexError, TypeError, ValueError):
        return 8.0

    if end_minutes <= start_minutes:
        end_minutes += 24 * 60

    return round(max(0, end_minutes - start_minutes) / 60, 2)


def is_present_attendance_status(status: str | None) -> bool:
    status_label = str(status or "").strip().lower()
    return (
        "present" in status_label
        or "late" in status_label
        or "undertime" in status_label
        or status_label in {"saved"}
    )


def resolve_log_employee_code(log, employee_codes_by_name: dict[str, str]) -> str:
    employee_code = str(log.employee_code or "").strip()
    if employee_code:
        return employee_code

    return employee_codes_by_name.get(normalize_employee_name(log.employee_name), "")


@router.get("", response_model=AttendanceListResponse)
def get_attendance_logs(
    _: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> AttendanceListResponse:
    logs = list_attendance_logs(db)
    return AttendanceListResponse(items=logs, total=len(logs))


@router.get("/duplicate-check")
def get_duplicate_attendance_check(
    employee_code: str = Query(...),
    work_date: str = Query(...),
    exclude_log_id: str | None = Query(default=None),
    log_action: str = Query(default="original"),
    _: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> dict:
    if str(log_action or "").strip().lower() == "correction":
        return {
            "is_duplicate": False,
            "matched_log_id": None,
        }

    matched_log = find_duplicate_attendance_log(
        db,
        employee_code=employee_code,
        work_date=work_date,
        exclude_log_id=exclude_log_id,
    )
    return {
        "is_duplicate": matched_log is not None,
        "matched_log_id": matched_log.log_id if matched_log else None,
    }


@router.get("/record/{log_id}", response_model=AttendanceResponse)
def get_attendance_record(
    log_id: str,
    _: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> AttendanceResponse:
    record = get_attendance_log_by_id(db, log_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance log not found")
    return AttendanceResponse.model_validate(record)


@router.post("", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
def create_attendance_record(
    payload: AttendanceCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> AttendanceResponse:
    if get_attendance_log_by_id(db, payload.log_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Attendance log ID already exists")

    if str(payload.log_action or "").strip().lower() != "correction":
        matched_log = find_duplicate_attendance_log(
            db,
            employee_code=payload.employee_code,
            work_date=payload.work_date,
        )
        if matched_log:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Attendance already exists for this employee on {payload.work_date} ({matched_log.log_id})",
            )

    payload_data = payload.model_dump()
    if get_holiday_by_date(db, payload.work_date):
        payload_data["holiday_work"] = "yes"

    try:
        record = create_attendance_log(db, payload_data)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error
    create_audit_log(
        db,
        module="Attendance",
        action=f"Create - {record.status}",
        record_id=record.log_id,
        actor=current_user,
        summary=f"Created attendance log for {record.employee_name} on {record.work_date}",
    )
    return AttendanceResponse.model_validate(record)


@router.put("/{log_id}", response_model=AttendanceResponse)
def update_attendance_record(
    log_id: str,
    payload: AttendanceUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> AttendanceResponse:
    record = get_attendance_log_by_id(db, log_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance log not found")

    try:
        payload_data = payload.model_dump()
        if get_holiday_by_date(db, payload.work_date):
            payload_data["holiday_work"] = "yes"
        updated_record = update_attendance_log(db, record, payload_data)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error
    create_audit_log(
        db,
        module="Attendance",
        action=f"Update - {updated_record.status}",
        record_id=updated_record.log_id,
        actor=current_user,
        summary=f"Updated attendance log for {updated_record.employee_name} on {updated_record.work_date}",
    )
    return AttendanceResponse.model_validate(updated_record)


@router.get("/summary")
def get_attendance_summary(
    work_date: str | None = Query(default=None),
    _: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> dict:
    logs = list_attendance_logs(db)
    try:
        target_date = date.fromisoformat(work_date) if work_date else date.today()
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="work_date must use YYYY-MM-DD format") from error

    target_date_text = target_date.isoformat()
    today_logs = [log for log in logs if log.work_date == target_date_text]
    holiday = get_holiday_by_date(db, target_date_text)
    scheduled_employees = [
        employee for employee in list_employees(db) if is_employee_scheduled_for_date(employee, target_date)
    ]
    employee_codes_by_name = {
        normalize_employee_name(f"{employee.first_name} {employee.last_name}"): employee.employee_code
        for employee in scheduled_employees
    }
    present_employee_codes = {
        resolve_log_employee_code(log, employee_codes_by_name)
        for log in today_logs
        if is_present_attendance_status(log.status)
        and resolve_log_employee_code(log, employee_codes_by_name)
    }
    logged_employee_codes = {
        resolve_log_employee_code(log, employee_codes_by_name)
        for log in today_logs
        if resolve_log_employee_code(log, employee_codes_by_name)
    }
    approved_leaves = approved_leave_by_employee_name(list_leave_requests(db), target_date)
    on_leave_employees = [
        employee
        for employee in scheduled_employees
        if employee.employee_code not in logged_employee_codes
        and normalize_employee_name(f"{employee.first_name} {employee.last_name}") in approved_leaves
    ]
    missing_employees = [
        employee
        for employee in scheduled_employees
        if employee.employee_code not in logged_employee_codes
        and employee not in on_leave_employees
    ]
    present_count = len(present_employee_codes)
    late_count = len([log for log in today_logs if "late" in log.status.lower()])
    correction_count = len([log for log in today_logs if log.log_action.lower() == "correction"])
    premium_count = len(
        [log for log in today_logs if log.rest_day_work.lower() == "yes" or log.holiday_work.lower() == "yes"]
    )
    incomplete_count = len([log for log in today_logs if log.status.lower() == "incomplete"])

    return {
        "total_logs": len(logs),
        "work_date": target_date_text,
        "holiday": {
            "name": holiday.name,
            "type": holiday.holiday_type,
        } if holiday else None,
        "today": {
            "expected": len(scheduled_employees),
            "present": present_count,
            "late": late_count,
            "corrections": correction_count,
            "premium": premium_count,
            "incomplete": incomplete_count,
            "on_leave": len(on_leave_employees),
            "absent": len(missing_employees),
            "missing": len(missing_employees),
        },
        "missing_today": [
            {
                "employee_code": employee.employee_code,
                "employee_name": f"{employee.first_name} {employee.last_name}",
                "shift_start": employee.default_shift_start,
                "shift_end": employee.default_shift_end,
            }
            for employee in missing_employees
        ],
        "on_leave_today": [
            {
                "employee_code": employee.employee_code,
                "employee_name": f"{employee.first_name} {employee.last_name}",
                "shift_start": employee.default_shift_start,
                "shift_end": employee.default_shift_end,
                "leave_type": approved_leaves[
                    normalize_employee_name(f"{employee.first_name} {employee.last_name}")
                ].leave_type,
                "leave_mode": approved_leaves[
                    normalize_employee_name(f"{employee.first_name} {employee.last_name}")
                ].leave_mode,
            }
            for employee in on_leave_employees
        ],
        "daily_roster": [
            {
                "employee_code": employee.employee_code,
                "employee_name": f"{employee.first_name} {employee.last_name}",
                "work_date": target_date_text,
                "shift_schedule": employee.work_schedule,
                "shift_start": employee.default_shift_start,
                "shift_end": employee.default_shift_end,
                "status": "On Leave"
                if employee in on_leave_employees
                else "Logged"
                if employee.employee_code in logged_employee_codes
                else "Absent",
                "leave_type": approved_leaves.get(
                    normalize_employee_name(f"{employee.first_name} {employee.last_name}")
                ).leave_type
                if normalize_employee_name(f"{employee.first_name} {employee.last_name}") in approved_leaves
                else None,
            }
            for employee in scheduled_employees
        ],
        "recent_logs": [
            {
                "log_id": log.log_id,
                "employee_code": log.employee_code,
                "employee_name": log.employee_name,
                "work_date": log.work_date,
                "clock_in": log.clock_in,
                "clock_out": log.clock_out,
                "status": log.status,
                "worked_hours": log.worked_hours,
                "payable_hours": log.payable_hours,
                "late_minutes": log.late_minutes,
                "undertime_minutes": log.undertime_minutes,
                "overtime_minutes": log.overtime_minutes,
            }
            for log in logs[:5]
        ],
    }


@router.get("/payroll-summary")
def get_attendance_payroll_summary(
    cutoff_start: str = Query(...),
    cutoff_end: str = Query(...),
    _: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> dict:
    try:
        start_date = date.fromisoformat(cutoff_start)
        end_date = date.fromisoformat(cutoff_end)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Cutoff dates must use YYYY-MM-DD format") from error

    if end_date < start_date:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Cutoff end cannot be earlier than cutoff start")

    logs = [
        log
        for log in list_attendance_logs(db)
        if cutoff_start <= log.work_date <= cutoff_end
    ]
    holidays = {holiday.holiday_date: holiday for holiday in list_holidays(db)}
    employees_by_code = {employee.employee_code: employee for employee in list_employees(db)}
    approved_leaves = list_leave_requests(db)

    rows_by_employee: dict[str, dict] = {}
    for employee in employees_by_code.values():
        rows_by_employee[employee.employee_code] = {
            "employee_code": employee.employee_code,
            "employee_name": f"{employee.first_name} {employee.last_name}",
            "regular_payable_hours": 0.0,
            "worked_hours": 0.0,
            "overtime_minutes": 0,
            "night_diff_minutes": 0,
            "late_minutes": 0,
            "undertime_minutes": 0,
            "holiday_work_days": 0,
            "rest_day_work_days": 0,
            "scheduled_days": 0,
            "scheduled_hours": 0.0,
            "present_days": 0,
            "leave_days": 0,
            "absent_days": 0,
            "incomplete_logs": 0,
        }

    for log in logs:
        row = rows_by_employee.setdefault(
            log.employee_code,
            {
                "employee_code": log.employee_code,
                "employee_name": log.employee_name,
                "regular_payable_hours": 0.0,
                "worked_hours": 0.0,
                "overtime_minutes": 0,
                "night_diff_minutes": 0,
                "late_minutes": 0,
                "undertime_minutes": 0,
                "holiday_work_days": 0,
                "rest_day_work_days": 0,
                "scheduled_days": 0,
                "scheduled_hours": 0.0,
                "present_days": 0,
                "leave_days": 0,
                "absent_days": 0,
                "incomplete_logs": 0,
            },
        )
        status_label = str(log.status or "").lower()
        row["regular_payable_hours"] += float(log.payable_hours or 0)
        row["worked_hours"] += float(log.worked_hours or 0)
        row["overtime_minutes"] += int(log.overtime_minutes or 0)
        row["night_diff_minutes"] += int(log.night_diff_minutes or 0)
        row["late_minutes"] += int(log.late_minutes or 0)
        row["undertime_minutes"] += int(log.undertime_minutes or 0)
        if is_present_attendance_status(status_label):
            row["present_days"] += 1
        if status_label == "incomplete":
            row["incomplete_logs"] += 1
        if str(log.holiday_work or "").lower() == "yes" or log.work_date in holidays:
            row["holiday_work_days"] += 1
        if str(log.rest_day_work or "").lower() == "yes":
            row["rest_day_work_days"] += 1

    cursor = start_date
    while cursor <= end_date:
        date_text = cursor.isoformat()
        day_logs = {log.employee_code for log in logs if log.work_date == date_text}
        day_leaves = approved_leave_by_employee_name(approved_leaves, cursor)

        for employee in employees_by_code.values():
            if not is_employee_scheduled_for_date(employee, cursor):
                continue

            row = rows_by_employee[employee.employee_code]
            row["scheduled_days"] += 1
            row["scheduled_hours"] += scheduled_hours_for_employee(employee)

            if employee.employee_code in day_logs:
                continue

            employee_name_key = normalize_employee_name(f"{employee.first_name} {employee.last_name}")
            if employee_name_key in day_leaves:
                row["leave_days"] += 1
            else:
                row["absent_days"] += 1

        cursor = date.fromordinal(cursor.toordinal() + 1)

    rows = sorted(rows_by_employee.values(), key=lambda item: item["employee_name"])
    totals = {
        "regular_payable_hours": round(sum(row["regular_payable_hours"] for row in rows), 2),
        "worked_hours": round(sum(row["worked_hours"] for row in rows), 2),
        "overtime_minutes": sum(row["overtime_minutes"] for row in rows),
        "night_diff_minutes": sum(row["night_diff_minutes"] for row in rows),
        "late_minutes": sum(row["late_minutes"] for row in rows),
        "undertime_minutes": sum(row["undertime_minutes"] for row in rows),
        "holiday_work_days": sum(row["holiday_work_days"] for row in rows),
        "rest_day_work_days": sum(row["rest_day_work_days"] for row in rows),
        "scheduled_days": sum(row["scheduled_days"] for row in rows),
        "scheduled_hours": round(sum(row["scheduled_hours"] for row in rows), 2),
        "present_days": sum(row["present_days"] for row in rows),
        "leave_days": sum(row["leave_days"] for row in rows),
        "absent_days": sum(row["absent_days"] for row in rows),
        "incomplete_logs": sum(row["incomplete_logs"] for row in rows),
    }

    for row in rows:
        row["regular_payable_hours"] = round(row["regular_payable_hours"], 2)
        row["worked_hours"] = round(row["worked_hours"], 2)
        row["scheduled_hours"] = round(row["scheduled_hours"], 2)

    return {
        "cutoff_start": cutoff_start,
        "cutoff_end": cutoff_end,
        "totals": totals,
        "rows": rows,
        "total": len(rows),
    }
