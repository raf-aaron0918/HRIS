from sqlalchemy.orm import Session

from app.models.employee import Employee


def list_employees(db: Session) -> list[Employee]:
    return db.query(Employee).order_by(Employee.last_name.asc(), Employee.first_name.asc()).all()


def get_employee_by_code(db: Session, employee_code: str) -> Employee | None:
    return db.query(Employee).filter(Employee.employee_code == employee_code).first()


def get_employee_by_email(db: Session, email: str) -> Employee | None:
    return db.query(Employee).filter(Employee.email == email).first()


def create_employee(db: Session, payload: dict) -> Employee:
    employee = Employee(**payload)
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def update_employee(db: Session, employee: Employee, payload: dict) -> Employee:
    for field, value in payload.items():
        setattr(employee, field, value)

    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee
