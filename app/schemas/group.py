from pydantic import BaseModel, ConfigDict, EmailStr


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
    member_emails: list[str] = []

    model_config = ConfigDict(from_attributes=True)
