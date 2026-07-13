from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.schemas.leave import LeaveCreate, LeaveListResponse, LeaveResponse, LeaveUpdate
from app.services.leave import create_leave_request, get_leave_request_by_id, list_leave_requests, update_leave_request

router = APIRouter()


@router.get("", response_model=LeaveListResponse)
def get_leave_requests(
    _: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> LeaveListResponse:
    requests = list_leave_requests(db)
    return LeaveListResponse(items=requests, total=len(requests))


@router.post("", response_model=LeaveResponse, status_code=status.HTTP_201_CREATED)
def create_leave_record(
    payload: LeaveCreate,
    _: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> LeaveResponse:
    if get_leave_request_by_id(db, payload.request_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Leave request ID already exists")

    record = create_leave_request(db, payload.model_dump())
    return LeaveResponse.model_validate(record)


@router.put("/{request_id}", response_model=LeaveResponse)
def update_leave_record(
    request_id: str,
    payload: LeaveUpdate,
    _: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> LeaveResponse:
    record = get_leave_request_by_id(db, request_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leave request not found")

    updated_record = update_leave_request(db, record, payload.model_dump())
    return LeaveResponse.model_validate(updated_record)


@router.get("/summary")
def get_leave_summary(
    _: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> dict:
    requests = list_leave_requests(db)
    pending_statuses = {"pending", "for hr review"}
    pending_count = len([request for request in requests if request.status.lower() in pending_statuses])
    approved_count = len([request for request in requests if request.status.lower() == "approved"])
    payroll_impact = sum(request.payroll_impact for request in requests)
    credits_used = sum(request.credits_used for request in requests)

    return {
        "total_requests": len(requests),
        "pending_requests": pending_count,
        "approved_requests": approved_count,
        "credits_used": credits_used,
        "payroll_impact": payroll_impact,
        "recent_requests": [
            {
                "request_id": request.request_id,
                "employee_name": request.employee_name,
                "leave_type": request.leave_type,
                "start_date": request.start_date,
                "end_date": request.end_date,
                "status": request.status,
            }
            for request in requests[:5]
        ],
    }
