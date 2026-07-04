from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.core.config import settings
from app.core.security import create_access_token
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import CurrentUserResponse
from app.services.auth import authenticate_user

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = authenticate_user(db, username=payload.username, password=payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(
        subject=user.username,
        expires_minutes=settings.access_token_expire_minutes,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=CurrentUserResponse.model_validate(user),
    )


@router.get("/me", response_model=CurrentUserResponse)
def read_current_user(current_user=Depends(get_current_active_user)) -> CurrentUserResponse:
    return CurrentUserResponse.model_validate(current_user)
