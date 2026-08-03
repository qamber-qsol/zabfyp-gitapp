from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.core.database import get_db
from app.core.security import get_password_hash
from app.models.comment import SystemComment
from app.models.group import ProjectGroup
from app.models.repository import GroupRepository, StudentGithubInvite
from app.models.student import Student, UserRole
from app.schemas.admin import (
    AdminActionResponse,
    AdminUserResponse,
    ForceInviteRequest,
    StudentOverrideUpdate,
    UserCreate,
)
from app.schemas.coordinator import StudentInfo
from app.schemas.group import GroupCreate, GroupResponse
from app.services.github import send_org_invite
from app.models.webhook import PushEvent

router = APIRouter(tags=["System Admin"], dependencies=[Depends(get_current_admin)])


@router.get("/dashboard", status_code=status.HTTP_200_OK)
def admin_dashboard():
    return {"message": "Admin dashboard operational"}


@router.post("/users", response_model=AdminUserResponse, status_code=status.HTTP_201_CREATED)
async def create_staff_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
) -> AdminUserResponse:
    clean_email = user_in.email.strip().lower()
    existing_user = db.query(Student).filter(Student.email == clean_email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists.",
        )

    target_role = UserRole.COORDINATOR if user_in.role == "coordinator" else UserRole.ADMIN

    new_user = Student(
        email=clean_email,
        hashed_password=get_password_hash(user_in.password),
        role=target_role,
        is_verified=True,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    role_str = new_user.role.value if hasattr(new_user.role, "value") else str(new_user.role)

    return AdminUserResponse(
        id=new_user.id,
        email=new_user.email,
        role=role_str,
        name=new_user.name,
        is_verified=new_user.is_verified,
    )


@router.patch("/students/{student_id}", response_model=StudentInfo, status_code=status.HTTP_200_OK)
async def override_student_details(
    student_id: int,
    update_data: StudentOverrideUpdate,
    db: Session = Depends(get_db),
) -> StudentInfo:
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} not found.",
        )

    if update_data.name is not None:
        student.name = update_data.name.strip()
    if update_data.email is not None:
        clean_email = update_data.email.strip().lower()
        # Check uniqueness if email changes
        existing = db.query(Student).filter(Student.email == clean_email, Student.id != student_id).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email address is already in use by another student.",
            )
        student.email = clean_email
    if "group_id" in update_data.model_fields_set:
        student.group_id = update_data.group_id
    if update_data.github_username is not None:
        student.github_username = update_data.github_username.strip()

    db.commit()
    db.refresh(student)

    return StudentInfo(
        id=student.id,
        name=student.name,
        email=student.email,
        reg_id=student.reg_id,
        is_verified=student.is_verified,
        github_username=student.github_username,
    )


@router.delete("/groups/{group_id}", response_model=AdminActionResponse, status_code=status.HTTP_200_OK)
async def delete_group_override(
    group_id: int,
    db: Session = Depends(get_db),
) -> AdminActionResponse:
    group = db.query(ProjectGroup).filter(ProjectGroup.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project group with id {group_id} not found.",
        )

    # Safety: unlink group_id from all student members
    db.query(Student).filter(Student.group_id == group_id).update({Student.group_id: None})

    # Unlink or remove repository and system comments associated with group
    db.query(GroupRepository).filter(GroupRepository.group_id == group_id).delete()
    db.query(SystemComment).filter(SystemComment.group_id == group_id).update({SystemComment.group_id: None})

    # Delete group record
    db.delete(group)
    db.commit()

    return AdminActionResponse(
        message=f"Project group with id {group_id} has been permanently deleted.",
        detail="Member students have been unlinked successfully.",
    )


@router.post("/github/force-invite", response_model=AdminActionResponse, status_code=status.HTTP_200_OK)
async def force_github_invite(
    request: ForceInviteRequest,
    db: Session = Depends(get_db),
) -> AdminActionResponse:
    student = db.query(Student).filter(Student.id == request.student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {request.student_id} not found.",
        )

    github_username = request.github_username or student.github_username
    if not github_username or not github_username.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student does not have a valid GitHub username configured.",
        )

    github_username = github_username.strip()

    # Determine repo name
    repo_name = f"fyp-student-{student.id}"
    if student.group_id:
        group = db.query(ProjectGroup).filter(ProjectGroup.id == student.group_id).first()
        if group:
            repo_name = group.repo_name or group.group_name or f"fyp-group-{group.id}"

    # Bypass standard checks and dispatch invite
    invite_sent = await send_org_invite(
        github_username=github_username,
        repo_name=repo_name,
    )

    # Save or update StudentGithubInvite
    invite = db.query(StudentGithubInvite).filter(StudentGithubInvite.student_id == student.id).first()
    new_invite_status = "sent" if invite_sent else "pending"

    if invite:
        invite.github_username = github_username
        invite.invite_status = new_invite_status
    else:
        invite = StudentGithubInvite(
            student_id=student.id,
            github_username=github_username,
            invite_status=new_invite_status,
        )
        db.add(invite)

    student.github_username = github_username
    db.commit()

    return AdminActionResponse(
        message=f"Force invitation sent successfully to '{github_username}'.",
        detail=f"Target repository: {repo_name}",
    )


@router.post("/groups", response_model=GroupResponse, status_code=status.HTTP_201_CREATED)
async def create_group_override(
    group_in: GroupCreate,
    db: Session = Depends(get_db),
) -> GroupResponse:
    new_group = ProjectGroup(
        group_name=group_in.group_name.strip(),
        team_name=group_in.team_name.strip() if group_in.team_name else None,
        status="approved"
    )
    db.add(new_group)
    db.commit()
    db.refresh(new_group)

    return GroupResponse(
        id=new_group.id,
        group_no=new_group.group_no,
        group_name=new_group.group_name,
        team_name=new_group.team_name,
        repo_name=new_group.repo_name,
        github_repo_url=new_group.github_repo_url,
        status=new_group.status,
        member_emails=[],
        partners=[]
    )


@router.get("/groups/{group_id}/logs", status_code=status.HTTP_200_OK)
async def get_group_logs(
    group_id: int,
    db: Session = Depends(get_db),
):
    group = db.query(ProjectGroup).filter(ProjectGroup.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project group with id {group_id} not found.",
        )
    
    events = db.query(PushEvent).filter(PushEvent.group_id == group_id).order_by(PushEvent.id.desc()).all()
    
    return [
        {
            "id": event.id,
            "commit_hash": event.commit_hash,
            "timestamp": event.timestamp,
            "approval_status": event.approval_status
        }
        for event in events
    ]
