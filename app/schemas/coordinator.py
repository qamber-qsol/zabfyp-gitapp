from pydantic import BaseModel, ConfigDict, field_validator


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
