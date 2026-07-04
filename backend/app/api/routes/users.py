from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_hr_admin
from app.schemas.user import CreateUserRequest, CurrentUserResponse, UserListResponse
from app.services.auth import create_user, get_user_by_email, get_user_by_username, list_users

router = APIRouter()


@router.get("", response_model=UserListResponse)
def read_users(
    _: object = Depends(require_hr_admin),
    db: Session = Depends(get_db),
) -> UserListResponse:
    users = list_users(db)
    return UserListResponse(items=[CurrentUserResponse.model_validate(user) for user in users])


@router.post("", response_model=CurrentUserResponse, status_code=status.HTTP_201_CREATED)
def create_account(
    payload: CreateUserRequest,
    _: object = Depends(require_hr_admin),
    db: Session = Depends(get_db),
) -> CurrentUserResponse:
    normalized_username = payload.username.strip()
    normalized_email = payload.email.strip().lower()

    if get_user_by_username(db, normalized_username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )

    if get_user_by_email(db, normalized_email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        )

    try:
        user = create_user(
            db,
            username=normalized_username,
            full_name=payload.full_name,
            email=normalized_email,
            password=payload.password,
            role=payload.role,
            is_active=payload.is_active,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid role selected",
        ) from exc

    return CurrentUserResponse.model_validate(user)
