from fastapi import APIRouter

from app.api.routes import attendance, auth, employees, leave, payroll, reports, users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(employees.router, prefix="/employees", tags=["employees"])
api_router.include_router(attendance.router, prefix="/attendance", tags=["attendance"])
api_router.include_router(leave.router, prefix="/leave", tags=["leave"])
api_router.include_router(payroll.router, prefix="/payroll", tags=["payroll"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
