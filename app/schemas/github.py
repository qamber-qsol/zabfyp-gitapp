from pydantic import BaseModel, ConfigDict


class InviteRequest(BaseModel):
    github_username: str


class InviteStatusResponse(BaseModel):
    github_username: str | None = None
    invite_status: str
    repo_name: str | None = None
    repo_status: str

    model_config = ConfigDict(from_attributes=True)
