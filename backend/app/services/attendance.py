from sqlalchemy.orm import Session

from app.models.attendance import AttendanceLog


def list_attendance_logs(db: Session) -> list[AttendanceLog]:
    return db.query(AttendanceLog).order_by(AttendanceLog.work_date.desc(), AttendanceLog.id.desc()).all()


def get_attendance_log_by_id(db: Session, log_id: str) -> AttendanceLog | None:
    return db.query(AttendanceLog).filter(AttendanceLog.log_id == log_id).first()


def find_duplicate_attendance_log(
    db: Session,
    *,
    employee_code: str,
    work_date: str,
    clock_in: str,
    clock_out: str,
    exclude_log_id: str | None = None,
) -> AttendanceLog | None:
    query = db.query(AttendanceLog).filter(
        AttendanceLog.employee_code == employee_code,
        AttendanceLog.work_date == work_date,
        AttendanceLog.clock_in == clock_in,
        AttendanceLog.clock_out == clock_out,
    )

    if exclude_log_id:
        query = query.filter(AttendanceLog.log_id != exclude_log_id)

    return query.order_by(AttendanceLog.id.desc()).first()


def create_attendance_log(db: Session, payload: dict) -> AttendanceLog:
    record = AttendanceLog(**payload)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def update_attendance_log(db: Session, record: AttendanceLog, payload: dict) -> AttendanceLog:
    for field, value in payload.items():
        setattr(record, field, value)

    db.add(record)
    db.commit()
    db.refresh(record)
    return record
