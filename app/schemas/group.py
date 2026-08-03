from pydantic import BaseModel, ConfigDict, EmailStr


class PartnerInfo(BaseModel):
    """Lightweight view of a group member (excluding the requesting student)."""
    id: int
    name: str | None = None          # maps to Student.name (not group column)
    email: str
    github_username: str | None = None
    invite_status: str | None = None

    model_config = ConfigDict(from_attributes=True)


class GroupCreate(BaseModel):
    """Payload for creating a new project group proposal."""
    group_name: str
    team_name: str | None = None
    member_emails: list[EmailStr] = []


class GroupResponse(BaseModel):
    """
    Read-only view of a ProjectGroup.
    All fields map 1-to-1 with the actual PostgreSQL project_groups columns.
    """
    id: int
    group_no: str | None = None
    group_name: str | None = None
    team_name: str | None = None
    repo_name: str | None = None
    github_repo_url: str | None = None
    status: str
    # Convenience list of member emails (computed, not a DB column)
    member_emails: list[str] = []
    # Rich partner objects
    partners: list[PartnerInfo] = []

    model_config = ConfigDict(from_attributes=True)
