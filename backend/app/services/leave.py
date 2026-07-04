from sqlalchemy.orm import Session

from app.models.leave import LeaveRequest


def list_leave_requests(db: Session) -> list[LeaveRequest]:
    return db.query(LeaveRequest).order_by(LeaveRequest.start_date.desc(), LeaveRequest.id.desc()).all()


def get_leave_request_by_id(db: Session, request_id: str) -> LeaveRequest | None:
    return db.query(LeaveRequest).filter(LeaveRequest.request_id == request_id).first()


def create_leave_request(db: Session, payload: dict) -> LeaveRequest:
    record = LeaveRequest(**payload)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def update_leave_request(db: Session, record: LeaveRequest, payload: dict) -> LeaveRequest:
    for field, value in payload.items():
        setattr(record, field, value)

    db.add(record)
    db.commit()
    db.refresh(record)
    return record
