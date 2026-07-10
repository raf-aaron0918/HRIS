from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CurrentUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    full_name: str
    email: str
    role: str
    is_active: bool


class CreateUserRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: str
    is_active: bool = True


class UserStatusUpdate(BaseModel):
    is_active: bool


class UserListResponse(BaseModel):
    items: list[CurrentUserResponse]
