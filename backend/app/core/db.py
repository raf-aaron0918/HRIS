from sqlalchemy import create_engine, inspect, text
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, sessionmaker

from app.core.seed import seed_defaults
from app.models import Base, Employee, User
from app.core.config import settings

def build_connect_args(database_url: str) -> dict:
    return {"check_same_thread": False} if database_url.startswith("sqlite") else {}


def create_engine_for_url(database_url: str):
    return create_engine(database_url, connect_args=build_connect_args(database_url))


def resolve_engine():
    primary_engine = create_engine_for_url(settings.database_url)

    if settings.database_url.startswith("sqlite"):
        return primary_engine, settings.database_url, False

    try:
        with primary_engine.connect() as connection:
            connection.execute(text("select 1"))
        return primary_engine, settings.database_url, False
    except OperationalError:
        fallback_engine = create_engine_for_url(settings.fallback_database_url)
        return fallback_engine, settings.fallback_database_url, True


engine, active_database_url, using_fallback_database = resolve_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, class_=Session)

EMPLOYEE_COLUMN_DEFINITIONS = {
    "middle_name": "VARCHAR(80)",
    "contact_number": "VARCHAR(40)",
    "birth_date": "VARCHAR(20)",
    "address": "VARCHAR(255)",
    "date_hired": "VARCHAR(20)",
    "branch": "VARCHAR(120)",
    "manager": "VARCHAR(120)",
    "account_status": "VARCHAR(50)",
    "onboarding_stage": "VARCHAR(50)",
    "movement_type": "VARCHAR(50)",
    "movement_effective_date": "VARCHAR(20)",
    "movement_remarks": "VARCHAR(255)",
    "offboarding_date": "VARCHAR(20)",
    "offboarding_reason": "VARCHAR(120)",
    "sss": "VARCHAR(20)",
    "philhealth": "VARCHAR(30)",
    "pagibig": "VARCHAR(20)",
    "tin": "VARCHAR(20)",
    "bank_account": "VARCHAR(255)",
    "emergency_contact": "VARCHAR(255)",
    "notes": "VARCHAR(500)",
}

LEAVE_COLUMN_DEFINITIONS = {
    "updated_at": "VARCHAR(40)",
    "attachment_data_url": "TEXT",
    "attachment_mime_type": "VARCHAR(120)",
}


def ensure_employee_columns() -> None:
    inspector = inspect(engine)
    if "employees" not in inspector.get_table_names():
        return

    existing_columns = {column["name"] for column in inspector.get_columns("employees")}
    missing_columns = {
        name: definition
        for name, definition in EMPLOYEE_COLUMN_DEFINITIONS.items()
        if name not in existing_columns
    }

    if not missing_columns:
        return

    with engine.begin() as connection:
        for column_name, definition in missing_columns.items():
            connection.execute(text(f"ALTER TABLE employees ADD COLUMN {column_name} {definition}"))


def ensure_leave_columns() -> None:
    inspector = inspect(engine)
    if "leave_requests" not in inspector.get_table_names():
        return

    existing_columns = {column["name"] for column in inspector.get_columns("leave_requests")}
    missing_columns = {
        name: definition
        for name, definition in LEAVE_COLUMN_DEFINITIONS.items()
        if name not in existing_columns
    }

    if not missing_columns:
        return

    with engine.begin() as connection:
        for column_name, definition in missing_columns.items():
            connection.execute(text(f"ALTER TABLE leave_requests ADD COLUMN {column_name} {definition}"))
        connection.execute(
            text(
                "UPDATE leave_requests "
                "SET updated_at = CURRENT_TIMESTAMP "
                "WHERE updated_at IS NULL OR updated_at = ''"
            )
        )


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    ensure_employee_columns()
    ensure_leave_columns()

    with SessionLocal() as db:
        seed_defaults(db)
        db.commit()
