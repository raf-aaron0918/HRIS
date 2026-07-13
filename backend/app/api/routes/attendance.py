from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.schemas.attendance import AttendanceCreate, AttendanceListResponse, AttendanceResponse, AttendanceUpdate
from app.services.attendance import (
    create_attendance_log,
    find_duplicate_attendance_log,
    get_attendance_log_by_id,
    list_attendance_logs,
    update_attendance_log,
)

router = APIRouter()


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
    clock_in: str = Query(...),
    clock_out: str = Query(...),
    exclude_log_id: str | None = Query(default=None),
    _: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> dict:
    matched_log = find_duplicate_attendance_log(
        db,
        employee_code=employee_code,
        work_date=work_date,
        clock_in=clock_in,
        clock_out=clock_out,
        exclude_log_id=exclude_log_id,
    )
    return {
        "is_duplicate": matched_log is not None,
        "matched_log_id": matched_log.log_id if matched_log else None,
    }


@router.post("", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
def create_attendance_record(
    payload: AttendanceCreate,
    _: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> AttendanceResponse:
    if get_attendance_log_by_id(db, payload.log_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Attendance log ID already exists")

    record = create_attendance_log(db, payload.model_dump())
    return AttendanceResponse.model_validate(record)


@router.put("/{log_id}", response_model=AttendanceResponse)
def update_attendance_record(
    log_id: str,
    payload: AttendanceUpdate,
    _: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> AttendanceResponse:
    record = get_attendance_log_by_id(db, log_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance log not found")

    updated_record = update_attendance_log(db, record, payload.model_dump())
    return AttendanceResponse.model_validate(updated_record)


@router.get("/summary")
def get_attendance_summary(
    _: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> dict:
    logs = list_attendance_logs(db)
    present_count = len([log for log in logs if log.status.lower() in {"present", "saved"}])
    late_count = len([log for log in logs if "late" in log.status.lower()])
    correction_count = len([log for log in logs if log.log_action == "correction"])
    premium_count = len([log for log in logs if log.rest_day_work == "yes" or log.holiday_work == "yes"])

    return {
        "total_logs": len(logs),
        "today": {
            "present": present_count,
            "late": late_count,
            "corrections": correction_count,
            "premium": premium_count,
        },
        "recent_logs": [
            {
                "log_id": log.log_id,
                "employee_code": log.employee_code,
                "employee_name": log.employee_name,
                "work_date": log.work_date,
                "clock_in": log.clock_in,
                "clock_out": log.clock_out,
                "status": log.status,
            }
            for log in logs[:5]
        ],
    }
