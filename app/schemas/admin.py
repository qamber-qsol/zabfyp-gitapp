from typing import Literal
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: Literal["coordinator", "admin"]


class StudentOverrideUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    group_id: int | None = None
    github_username: str | None = None


class ForceInviteRequest(BaseModel):
    student_id: int
    github_username: str | None = None


class AdminUserResponse(BaseModel):
    id: int
    email: str
    role: str
    name: str | None = None
    is_verified: bool = True

    model_config = ConfigDict(from_attributes=True)


class AdminActionResponse(BaseModel):
    message: str
    detail: str | None = None

class CreateUserRequest(BaseModel):
    name: str
    email: str
    identifier_id: str
    role: str

class AssignStudentRequest(BaseModel):
    student_id: int
    github_username: str

class GroupStatusUpdate(BaseModel):
    status: str
