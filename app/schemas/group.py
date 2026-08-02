from pydantic import BaseModel, ConfigDict, EmailStr


class PartnerInfo(BaseModel):
    """Lightweight view of a group member (excluding the requesting student)."""
    id: int
    name: str | None = None
    email: str
    github_username: str | None = None
    invite_status: str | None = None

    model_config = ConfigDict(from_attributes=True)


class GroupCreate(BaseModel):
    name: str
    project_title: str
    description: str
    member_emails: list[EmailStr] = []


class GroupResponse(BaseModel):
    id: int
    name: str
    project_title: str | None = None
    description: str | None = None
    status: str
    repo_name: str | None = None
    github_repo_url: str | None = None
    # Flat email list kept for backward compat (coordinator views, etc.)
    member_emails: list[str] = []
    # Rich partner objects (name + email + invite status)
    partners: list[PartnerInfo] = []

    model_config = ConfigDict(from_attributes=True)
