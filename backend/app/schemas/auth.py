from pydantic import BaseModel

from app.schemas.user import CurrentUserResponse


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: CurrentUserResponse
