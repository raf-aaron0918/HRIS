from sqlalchemy.orm import Session

from app.models.attendance import AttendanceLog


def list_attendance_logs(db: Session) -> list[AttendanceLog]:
    return db.query(AttendanceLog).order_by(AttendanceLog.work_date.desc(), AttendanceLog.id.desc()).all()


def get_attendance_log_by_id(db: Session, log_id: str) -> AttendanceLog | None:
    return db.query(AttendanceLog).filter(AttendanceLog.log_id == log_id).first()


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
