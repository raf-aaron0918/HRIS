from pydantic import BaseModel, ConfigDict


class AuditLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    module: str
    action: str
    record_id: str
    actor: str
    actor_role: str | None = None
    summary: str | None = None
    created_at: str


class AuditLogListResponse(BaseModel):
    items: list[AuditLogResponse]
    total: int
