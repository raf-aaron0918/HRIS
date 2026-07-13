from sqlalchemy.orm import Session

from app.models.holiday import Holiday


def list_holidays(db: Session) -> list[Holiday]:
    return db.query(Holiday).order_by(Holiday.holiday_date.desc(), Holiday.id.desc()).all()


def get_holiday_by_id(db: Session, holiday_id: str) -> Holiday | None:
    return db.query(Holiday).filter(Holiday.holiday_id == holiday_id).first()


def get_holiday_by_date(db: Session, holiday_date: str) -> Holiday | None:
    return db.query(Holiday).filter(Holiday.holiday_date == holiday_date).first()


def create_holiday(db: Session, payload: dict) -> Holiday:
    record = Holiday(**payload)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def update_holiday(db: Session, record: Holiday, payload: dict) -> Holiday:
    for field, value in payload.items():
        setattr(record, field, value)

    db.add(record)
    db.commit()
    db.refresh(record)
    return record
