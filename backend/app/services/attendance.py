from sqlalchemy.orm import Session

from app.models.attendance import AttendanceLog
from app.models.employee import Employee
from app.models.leave import LeaveRequest

MINUTES_PER_DAY = 24 * 60
WEEKDAY_KEYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
DERIVED_ATTENDANCE_FIELDS = {
    "status",
    "worked_hours",
    "payable_hours",
    "late_minutes",
    "undertime_minutes",
    "overtime_minutes",
    "night_diff_minutes",
}


def is_active_employee(employee: Employee) -> bool:
    account_status = str(employee.account_status or "").strip().lower()
    employment_status = str(employee.employment_status or "").strip().lower()
    return account_status == "active" or (not account_status and employment_status in {"regular", "probationary", "contractual"})


def is_employee_scheduled_for_date(employee: Employee, work_date) -> bool:
    work_days = {
        day.strip().lower()
        for day in str(employee.work_days or "mon,tue,wed,thu,fri").split(",")
        if day.strip()
    }
    weekday_key = WEEKDAY_KEYS[work_date.weekday()]
    return is_active_employee(employee) and weekday_key in work_days


def normalize_employee_name(value: str | None) -> str:
    return " ".join(str(value or "").strip().lower().split())


def approved_leave_by_employee_name(
    leave_requests: list[LeaveRequest],
    work_date,
) -> dict[str, LeaveRequest]:
    approved_leaves = {}
    target_date = work_date.isoformat()

    for request in leave_requests:
        if str(request.status or "").strip().lower() != "approved":
            continue
        if request.start_date <= target_date <= request.end_date:
            approved_leaves[normalize_employee_name(request.employee_name)] = request

    return approved_leaves


def _parse_time(value: str | None, field_name: str, *, required: bool = False) -> int | None:
    normalized = str(value or "").strip()
    if not normalized:
        if required:
            raise ValueError(f"{field_name} is required")
        return None

    try:
        hour_text, minute_text = normalized.split(":", maxsplit=1)
        hour = int(hour_text)
        minute = int(minute_text)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{field_name} must use HH:MM format") from error

    if not 0 <= hour <= 23 or not 0 <= minute <= 59:
        raise ValueError(f"{field_name} must be a valid time")
    return hour * 60 + minute


def _hours(minutes: int) -> float:
    return round(minutes / 60, 2)


def _night_minutes(start: int, end: int) -> int:
    total = 0
    for minute in range(start, end):
        hour = (minute // 60) % 24
        if hour >= 22 or hour < 6:
            total += 1
    return total


def calculate_attendance(payload: dict) -> dict[str, str | int | float]:
    shift_start = _parse_time(payload.get("shift_start"), "Shift start", required=True)
    shift_end_raw = _parse_time(payload.get("shift_end"), "Shift end", required=True)
    clock_in_raw = _parse_time(payload.get("clock_in"), "Clock in")
    clock_out_raw = _parse_time(payload.get("clock_out"), "Clock out")
    break_out_raw = _parse_time(payload.get("break_out"), "Break out")
    break_in_raw = _parse_time(payload.get("break_in"), "Break in")
    grace_minutes = max(0, int(payload.get("grace_minutes") or 0))

    assert shift_start is not None and shift_end_raw is not None
    overnight_shift = shift_end_raw <= shift_start
    shift_end = shift_end_raw + MINUTES_PER_DAY if overnight_shift else shift_end_raw
    scheduled_minutes = shift_end - shift_start

    if (break_out_raw is None) != (break_in_raw is None):
        raise ValueError("Break out and break in must be provided together")

    if clock_in_raw is None or clock_out_raw is None:
        late_minutes = 0
        if clock_in_raw is not None:
            clock_in = clock_in_raw
            if overnight_shift and clock_in_raw <= shift_end_raw:
                clock_in += MINUTES_PER_DAY
            late_minutes = max(0, clock_in - shift_start - grace_minutes)

        return {
            "status": "Incomplete",
            "worked_hours": 0,
            "payable_hours": 0,
            "late_minutes": late_minutes,
            "undertime_minutes": 0,
            "overtime_minutes": 0,
            "night_diff_minutes": 0,
        }

    if not overnight_shift and clock_out_raw < clock_in_raw:
        raise ValueError("Clock out cannot be earlier than clock in for a same-day shift")

    clock_in = clock_in_raw
    if overnight_shift and clock_in_raw <= shift_end_raw:
        clock_in += MINUTES_PER_DAY

    clock_out = clock_out_raw
    while clock_out < clock_in:
        clock_out += MINUTES_PER_DAY

    if clock_out - clock_in > MINUTES_PER_DAY:
        raise ValueError("An attendance record cannot exceed 24 hours")

    break_minutes = 0
    if break_out_raw is not None and break_in_raw is not None:
        break_out = break_out_raw
        while break_out < clock_in:
            break_out += MINUTES_PER_DAY
        break_in = break_in_raw
        while break_in < break_out:
            break_in += MINUTES_PER_DAY
        if break_out < clock_in or break_in > clock_out or break_in <= break_out:
            raise ValueError("Break times must fall between clock in and clock out")
        break_minutes = break_in - break_out

    worked_minutes = clock_out - clock_in - break_minutes
    if worked_minutes < 0:
        raise ValueError("Break duration cannot exceed worked time")

    late_minutes = max(0, clock_in - shift_start - grace_minutes)
    undertime_minutes = max(0, shift_end - clock_out)
    overtime_minutes = max(0, clock_out - shift_end)
    payable_minutes = min(worked_minutes, scheduled_minutes)

    if late_minutes and undertime_minutes:
        attendance_status = "Late / Undertime"
    elif late_minutes:
        attendance_status = "Late"
    elif undertime_minutes:
        attendance_status = "Undertime"
    else:
        attendance_status = "Present"

    return {
        "status": attendance_status,
        "worked_hours": _hours(worked_minutes),
        "payable_hours": _hours(payable_minutes),
        "late_minutes": late_minutes,
        "undertime_minutes": undertime_minutes,
        "overtime_minutes": overtime_minutes,
        "night_diff_minutes": _night_minutes(clock_in, clock_out),
    }


def apply_attendance_rules(payload: dict) -> dict:
    normalized_payload = {
        field: value for field, value in payload.items() if field not in DERIVED_ATTENDANCE_FIELDS
    }
    normalized_payload["grace_minutes"] = max(0, int(normalized_payload.get("grace_minutes") or 0))
    normalized_payload["clock_in"] = str(normalized_payload.get("clock_in") or "").strip()
    normalized_payload["clock_out"] = str(normalized_payload.get("clock_out") or "").strip()
    normalized_payload.update(calculate_attendance(normalized_payload))
    return normalized_payload


def list_attendance_logs(db: Session) -> list[AttendanceLog]:
    return db.query(AttendanceLog).order_by(AttendanceLog.work_date.desc(), AttendanceLog.id.desc()).all()


def get_attendance_log_by_id(db: Session, log_id: str) -> AttendanceLog | None:
    return db.query(AttendanceLog).filter(AttendanceLog.log_id == log_id).first()


def find_duplicate_attendance_log(
    db: Session,
    *,
    employee_code: str,
    work_date: str,
    exclude_log_id: str | None = None,
    include_corrections: bool = False,
) -> AttendanceLog | None:
    query = db.query(AttendanceLog).filter(
        AttendanceLog.employee_code == employee_code,
        AttendanceLog.work_date == work_date,
    )

    if not include_corrections:
        query = query.filter(AttendanceLog.log_action != "correction")

    if exclude_log_id:
        query = query.filter(AttendanceLog.log_id != exclude_log_id)

    return query.order_by(AttendanceLog.id.desc()).first()


def create_attendance_log(db: Session, payload: dict) -> AttendanceLog:
    record = AttendanceLog(**apply_attendance_rules(payload))
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def update_attendance_log(db: Session, record: AttendanceLog, payload: dict) -> AttendanceLog:
    for field, value in apply_attendance_rules(payload).items():
        setattr(record, field, value)

    db.add(record)
    db.commit()
    db.refresh(record)
    return record
