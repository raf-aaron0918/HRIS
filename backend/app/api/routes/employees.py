from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db, require_hr_admin
from app.models.user import User
from app.schemas.employee import EmployeeCreate, EmployeeListResponse, EmployeeResponse, EmployeeUpdate
from app.services.employee import create_employee, get_employee_by_code, get_employee_by_email, list_employees, update_employee

router = APIRouter()


@router.get("", response_model=EmployeeListResponse)
def get_employees(
    db: Session = Depends(get_db),
) -> EmployeeListResponse:
    employees = list_employees(db)
    return EmployeeListResponse(items=employees, total=len(employees))


@router.post("", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee_record(
    payload: EmployeeCreate,
    _: User = Depends(require_hr_admin),
    db: Session = Depends(get_db),
) -> EmployeeResponse:
    if get_employee_by_code(db, payload.employee_code):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Employee code already exists")

    if get_employee_by_email(db, payload.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Employee email already exists")

    employee = create_employee(db, payload.model_dump())
    return EmployeeResponse.model_validate(employee)


@router.put("/{employee_code}", response_model=EmployeeResponse)
def update_employee_record(
    employee_code: str,
    payload: EmployeeUpdate,
    _: User = Depends(require_hr_admin),
    db: Session = Depends(get_db),
) -> EmployeeResponse:
    employee = get_employee_by_code(db, employee_code)
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    existing_email_owner = get_employee_by_email(db, payload.email)
    if existing_email_owner and existing_email_owner.employee_code != employee_code:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Employee email already exists")

    updated_employee = update_employee(db, employee, payload.model_dump())
    return EmployeeResponse.model_validate(updated_employee)
