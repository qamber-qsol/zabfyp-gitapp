from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator

from app.schemas.group import GroupResponse


class GroupStatusUpdate(BaseModel):
    status: str
    feedback: str | None = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        clean_v = v.strip().lower()
        if clean_v not in ("approved", "rejected"):
            raise ValueError("Status must be either 'approved' or 'rejected'.")
        return clean_v


class GroupStatusUpdateResponse(BaseModel):
    id: int
    name: str
    project_title: str | None = None
    description: str | None = None
    status: str
    member_emails: list[str] = []
    feedback: str | None = None

    model_config = ConfigDict(from_attributes=True)


class DashboardMetricsResponse(BaseModel):
    total_students: int
    total_groups: int
    approved_groups: int
    rejected_groups: int
    pending_github_invites: int
    active_repositories: int


class StudentInfo(BaseModel):
    id: int
    name: str | None = None
    email: str
    reg_id: str | None = None
    is_verified: bool
    github_username: str | None = None

    model_config = ConfigDict(from_attributes=True)


class CommentSchema(BaseModel):
    id: int
    content: str
    author_id: int | None = None
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class GroupRepositorySchema(BaseModel):
    id: int
    group_id: int
    repo_name: str
    status: str

    model_config = ConfigDict(from_attributes=True)


class StudentGithubInviteSchema(BaseModel):
    id: int
    student_id: int
    github_username: str
    invite_status: str

    model_config = ConfigDict(from_attributes=True)


class GroupDeepDiveResponse(BaseModel):
    group_info: GroupResponse
    members: list[StudentInfo] = []
    comments: list[CommentSchema] = []
    repository_info: GroupRepositorySchema | None = None
    invite_statuses: list[StudentGithubInviteSchema] = []

    model_config = ConfigDict(from_attributes=True)

