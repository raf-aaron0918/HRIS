from sqlalchemy.orm import Session

from app.core.security import get_password_hash
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
