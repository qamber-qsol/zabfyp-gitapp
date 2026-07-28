from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_student
from app.core.database import get_db
from app.models.group import ProjectGroup
from app.models.repository import GroupRepository, StudentGithubInvite
from app.models.student import Student
from app.schemas.github import InviteRequest, InviteStatusResponse
from app.services.github import send_org_invite

router = APIRouter(tags=["GitHub Integration"])


@router.post("/invite", response_model=InviteStatusResponse, status_code=status.HTTP_200_OK)
async def request_github_invite(
    invite_in: InviteRequest,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
) -> InviteStatusResponse:
    if current_student.group_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student is not a member of any project group.",
        )

    group = db.query(ProjectGroup).filter(ProjectGroup.id == current_student.group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project group not found.",
        )

    if (group.status or "").lower() != "approved":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Group proposal must be approved before requesting a GitHub repository invite.",
        )

    # Get or create GroupRepository
    repo = db.query(GroupRepository).filter(GroupRepository.group_id == group.id).first()
    if not repo:
        repo_name = group.repo_name or group.name or f"fyp-group-{group.id}"
        repo = GroupRepository(
            group_id=group.id,
            repo_name=repo_name,
            status="pending_creation",
        )
        db.add(repo)
        db.flush()

    # Call service stub to dispatch GitHub invite
    invite_sent = await send_org_invite(
        github_username=invite_in.github_username,
        repo_name=repo.repo_name,
    )

    # Update or create student's GitHub invite record
    invite = db.query(StudentGithubInvite).filter(StudentGithubInvite.student_id == current_student.id).first()
    new_invite_status = "sent" if invite_sent else "pending"

    if invite:
        invite.github_username = invite_in.github_username
        invite.invite_status = new_invite_status
    else:
        invite = StudentGithubInvite(
            student_id=current_student.id,
            github_username=invite_in.github_username,
            invite_status=new_invite_status,
        )
        db.add(invite)

    current_student.github_username = invite_in.github_username

    db.commit()
    db.refresh(repo)
    db.refresh(invite)

    return InviteStatusResponse(
        github_username=invite.github_username,
        invite_status=invite.invite_status,
        repo_name=repo.repo_name,
        repo_status=repo.status,
    )


@router.get("/status", response_model=InviteStatusResponse, status_code=status.HTTP_200_OK)
async def get_github_status(
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
) -> InviteStatusResponse:
    if current_student.group_id is None:
        return InviteStatusResponse(
            github_username=current_student.github_username,
            invite_status="not_requested",
            repo_name=None,
            repo_status="not_created",
        )

    repo = db.query(GroupRepository).filter(GroupRepository.group_id == current_student.group_id).first()
    invite = db.query(StudentGithubInvite).filter(StudentGithubInvite.student_id == current_student.id).first()

    return InviteStatusResponse(
        github_username=invite.github_username if invite else current_student.github_username,
        invite_status=invite.invite_status if invite else "not_requested",
        repo_name=repo.repo_name if repo else None,
        repo_status=repo.status if repo else "pending_creation",
    )
