from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.schemas.holiday import HolidayCreate, HolidayListResponse, HolidayResponse, HolidayUpdate
from app.services.audit import create_audit_log
from app.services.holiday import (
    create_holiday,
    get_holiday_by_date,
    get_holiday_by_id,
    list_holidays,
    update_holiday,
)

router = APIRouter()


@router.get("", response_model=HolidayListResponse)
def get_holidays(
    _: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> HolidayListResponse:
    records = list_holidays(db)
    return HolidayListResponse(items=records, total=len(records))


@router.post("", response_model=HolidayResponse, status_code=status.HTTP_201_CREATED)
def create_holiday_record(
    payload: HolidayCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> HolidayResponse:
    if get_holiday_by_id(db, payload.holiday_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Holiday ID already exists")
    existing_date = get_holiday_by_date(db, payload.holiday_date)
    if existing_date:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Holiday date already exists")

    record = create_holiday(db, payload.model_dump())
    create_audit_log(
        db,
        module="Holiday",
        action="Create",
        record_id=record.holiday_id,
        actor=current_user,
        summary=f"Created holiday {record.name} on {record.holiday_date}",
    )
    return HolidayResponse.model_validate(record)


@router.put("/{holiday_id}", response_model=HolidayResponse)
def update_holiday_record(
    holiday_id: str,
    payload: HolidayUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> HolidayResponse:
    record = get_holiday_by_id(db, holiday_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Holiday not found")

    existing_date = get_holiday_by_date(db, payload.holiday_date)
    if existing_date and existing_date.holiday_id != holiday_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Holiday date already exists")

    updated_record = update_holiday(db, record, payload.model_dump())
    create_audit_log(
        db,
        module="Holiday",
        action="Update",
        record_id=updated_record.holiday_id,
        actor=current_user,
        summary=f"Updated holiday {updated_record.name} on {updated_record.holiday_date}",
    )
    return HolidayResponse.model_validate(updated_record)
