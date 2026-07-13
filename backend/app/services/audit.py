from datetime import datetime, timezone

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.audit import AuditLog
from app.models.user import User


def current_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def actor_label(user: User | None) -> str:
    if not user:
        return "System"
    return user.full_name or user.email or user.username


def create_audit_log(
    db: Session,
    *,
    module: str,
    action: str,
    record_id: str,
    actor: User | None,
    summary: str | None = None,
) -> AuditLog | None:
    log = AuditLog(
        module=module,
        action=action,
        record_id=record_id,
        actor=actor_label(actor),
        actor_role=str(actor.role.value if actor and hasattr(actor.role, "value") else actor.role if actor else ""),
        summary=summary,
        created_at=current_timestamp(),
    )
    try:
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
    except SQLAlchemyError:
        db.rollback()
        return None


def list_audit_logs(db: Session, *, limit: int = 100) -> list[AuditLog]:
    return db.query(AuditLog).order_by(AuditLog.created_at.desc(), AuditLog.id.desc()).limit(limit).all()
