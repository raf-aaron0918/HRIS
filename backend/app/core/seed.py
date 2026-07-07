from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.employee import Employee
from app.models.user import User, UserRole

SEEDED_USERS = [
    {
        "username": "admin",
        "full_name": "System Administrator",
        "email": "admin@hris.local",
        "hashed_password": lambda: get_password_hash("admin123"),
        "role": UserRole.hr_admin,
        "is_active": True,
    }
]


def seed_defaults(db: Session) -> None:
    if not db.query(User).first():
        db.add_all(
            [
                User(
                    username=item["username"],
                    full_name=item["full_name"],
                    email=item["email"],
                    hashed_password=item["hashed_password"](),
                    role=item["role"],
                    is_active=item["is_active"],
                )
                for item in SEEDED_USERS
            ]
        )

    if not db.query(Employee).first():
        db.add_all(
            [
                Employee(
                    employee_code="EMP-1001",
                    first_name="Ariane",
                    last_name="Dela Cruz",
                    email="ariane@hris.local",
                    department="Administration",
                    position="HR Officer",
                    branch="Main Branch",
                    employment_status="Regular",
                    account_status="Active",
                    onboarding_stage="Completed",
                ),
                Employee(
                    employee_code="EMP-1002",
                    first_name="Mark",
                    last_name="Santos",
                    email="mark@hris.local",
                    department="Operations",
                    position="Operations Lead",
                    branch="Main Branch",
                    employment_status="Regular",
                    account_status="Active",
                    onboarding_stage="Completed",
                ),
            ]
        )
