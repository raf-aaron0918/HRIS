from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_hr_admin
from app.models.user import User
from app.schemas.audit import AuditLogListResponse
from app.services.audit import list_audit_logs

router = APIRouter()


@router.get("", response_model=AuditLogListResponse)
def get_audit_logs(
    limit: int = Query(default=100, ge=1, le=500),
    _: User = Depends(require_hr_admin),
    db: Session = Depends(get_db),
) -> AuditLogListResponse:
    logs = list_audit_logs(db, limit=limit)
    return AuditLogListResponse(items=logs, total=len(logs))
