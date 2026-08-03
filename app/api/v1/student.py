from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session, joinedload

from app.api.deps import get_current_student
from app.core.database import get_db
from app.models.group import ProjectGroup
from app.models.repository import GroupRepository, StudentGithubInvite
from app.models.student import Student
from app.schemas.github import InviteStatusResponse
from app.schemas.group import GroupResponse, PartnerInfo
from app.services.github import send_org_invite

router = APIRouter(tags=["Students"])


# ---------------------------------------------------------------------------
# Pydantic response schema
# ---------------------------------------------------------------------------
class StudentProfileResponse(BaseModel):
    id: int
    reg_id: str | None = None
    name: str | None = None
    email: str
    role: str
    is_verified: bool
    github_username: str | None = None
    invite_status: str | None = None
    group_id: int | None = None
    group: GroupResponse | None = None

    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# Helper: build GroupResponse from a directly-queried ProjectGroup ORM object.
# Only touches the 7 columns that physically exist in PostgreSQL.
# ---------------------------------------------------------------------------
def _build_group_response(group: ProjectGroup, current_student_id: int) -> GroupResponse:
    partners = [
        PartnerInfo(
            id=s.id,
            name=s.name,
            email=s.email,
            github_username=s.github_username,
            invite_status=s.invite_status,
        )
        for s in group.students
        if s.id != current_student_id
    ]
    member_emails = [s.email for s in group.students if s.email]

    return GroupResponse(
        id=group.id,
        group_no=group.group_no,
        group_name=group.group_name,
        team_name=group.team_name,
        repo_name=group.repo_name,
        github_repo_url=group.github_repo_url,
        status=group.status,
        member_emails=member_emails,
        partners=partners,
    )


# ---------------------------------------------------------------------------
# GET /students/me
#
# FIX: Do NOT use a nested joinedload(Student.group).joinedload(...) chain.
# SQLAlchemy's identity map means the Student object loaded by the
# get_current_student dependency is cached in the session WITHOUT its group
# relationship loaded. A subsequent re-query for the same Student ID returns
# that same cached object, leaving group=None even when group_id is set.
#
# Instead, we query the Student for its scalar fields, then separately and
# explicitly query the ProjectGroup by group_id. This is bulletproof.
# ---------------------------------------------------------------------------
@router.get("/me", response_model=StudentProfileResponse, status_code=status.HTTP_200_OK)
async def get_my_profile(
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
) -> StudentProfileResponse:
    """
    Return the authenticated student's full profile, including their assigned
    project group details and the names/emails of all group partners.
    """
    # Expire the cached student object so SQLAlchemy re-reads all scalar columns
    db.expire(current_student)
    db.refresh(current_student)

    group_response: GroupResponse | None = None

    if current_student.group_id:
        # Query the group directly — avoids the identity-map problem entirely
        group = (
            db.query(ProjectGroup)
            .options(joinedload(ProjectGroup.students))
            .filter(ProjectGroup.id == current_student.group_id)
            .first()
        )
        if group:
            group_response = _build_group_response(group, current_student.id)

    role_str = (
        current_student.role.value
        if hasattr(current_student.role, "value")
        else str(current_student.role)
    )

    return StudentProfileResponse(
        id=current_student.id,
        reg_id=current_student.reg_id,
        name=current_student.name,
        email=current_student.email,
        role=role_str,
        is_verified=current_student.is_verified,
        github_username=current_student.github_username,
        invite_status=current_student.invite_status,
        group_id=current_student.group_id,
        group=group_response,
    )


# ---------------------------------------------------------------------------
# POST /students/me/github-invite
# One-click GitHub org invite dispatched to the student's registered email
# ---------------------------------------------------------------------------
@router.post(
    "/me/github-invite",
    response_model=InviteStatusResponse,
    status_code=status.HTTP_200_OK,
)
async def send_my_github_invite(
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
) -> InviteStatusResponse:
    """
    Trigger a GitHub organization invite for the authenticated student using
    their registered email address. No request body is required.

    Guards:
    - Student must belong to a group.
    - The group must be in 'approved' status.
    """
    db.refresh(current_student)

    if current_student.group_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not assigned to any project group yet.",
        )

    group = (
        db.query(ProjectGroup)
        .filter(ProjectGroup.id == current_student.group_id)
        .first()
    )
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assigned project group was not found.",
        )

    if (group.status or "").lower() != "approved":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your group proposal must be approved before a GitHub invite can be dispatched.",
        )

    repo = db.query(GroupRepository).filter(GroupRepository.group_id == group.id).first()
    if not repo:
        repo_name = group.repo_name or group.group_name or f"fyp-group-{group.id}"
        repo = GroupRepository(
            group_id=group.id,
            repo_name=repo_name,
            status="pending_creation",
        )
        db.add(repo)
        db.flush()

    invite_sent = await send_org_invite(
        github_username=current_student.email,
        repo_name=repo.repo_name,
    )

    new_status = "sent" if invite_sent else "pending"

    invite = (
        db.query(StudentGithubInvite)
        .filter(StudentGithubInvite.student_id == current_student.id)
        .first()
    )
    if invite:
        invite.invite_status = new_status
    else:
        invite = StudentGithubInvite(
            student_id=current_student.id,
            github_username=current_student.github_username or current_student.email,
            invite_status=new_status,
        )
        db.add(invite)

    current_student.invite_status = new_status

    db.commit()
    db.refresh(repo)
    db.refresh(invite)

    return InviteStatusResponse(
        github_username=invite.github_username,
        invite_status=invite.invite_status,
        repo_name=repo.repo_name,
        repo_status=repo.status,
    )
