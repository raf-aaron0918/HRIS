# HRIS FastAPI Backend

This folder contains the Python backend for the HRIS Vue frontend.

## Stack

- FastAPI
- SQLAlchemy 2
- Alembic
- Pydantic Settings
- JWT authentication
- SQLite for local development

## Current Structure

- `app/api/routes`: FastAPI route handlers
- `app/core`: config, database bootstrapping, security helpers
- `app/models`: SQLAlchemy models
- `app/schemas`: request/response schemas
- `app/services/auth.py`: authentication queries and password verification
- `app/services/employee.py`: employee CRUD data access

## Quick Start

1. Create a virtual environment
2. Install dependencies from `backend/requirements.txt`
3. Copy `backend/.env.example` to `backend/.env`
4. Run the API

```bash
python -m pip install -r backend/requirements.txt
npm run dev:api
```

## Render Deployment

This backend is ready to deploy on Render as a Python web service.

Recommended settings:

- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Root directory: `backend`

Required environment variables:

- `APP_ENV=production`
- `APP_DEBUG=false`
- `SECRET_KEY` set to a long random value
- `BACKEND_CORS_ORIGINS` set to your Vercel frontend URL
- `DATABASE_URL` set to a Postgres connection string

If you want a ready-made blueprint, use the root `render.yaml`.

## Default Local Login

- Username: `admin`
- Password: `admin123`

No sample employee records are seeded automatically. Create employees from the app or API.

## First API Endpoints

- `GET /`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `GET /api/v1/employees`
- `POST /api/v1/employees`
- `PUT /api/v1/employees/{employee_code}`
- `GET /api/v1/attendance`
- `POST /api/v1/attendance`
- `PUT /api/v1/attendance/{log_id}`
- `GET /api/v1/attendance/summary`
- `GET /api/v1/leave`
- `POST /api/v1/leave`
- `PUT /api/v1/leave/{request_id}`
- `GET /api/v1/leave/summary`
- `GET /api/v1/payroll`
- `POST /api/v1/payroll`
- `PUT /api/v1/payroll/{payroll_run_id}`
- `GET /api/v1/payroll/summary`
- `GET /api/v1/reports`
- `GET /api/v1/reports/data?report_type=employee`
