from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload

from app.api.deps import get_current_coordinator
from app.core.database import get_db
from app.models.comment import SystemComment
from app.models.group import ProjectGroup
from app.models.repository import GroupRepository, StudentGithubInvite
from app.models.student import Student
from app.schemas.coordinator import (
    CommentSchema,
    GroupDeepDiveResponse,
    GroupRepositorySchema,
    GroupStatusUpdate,
    GroupStatusUpdateResponse,
    StudentGithubInviteSchema,
    StudentInfo,
)
from app.schemas.group import GroupResponse, PartnerInfo
from app.services.email import send_group_status_email

router = APIRouter(tags=["Coordinator Dashboard"])


@router.get("/groups", response_model=list[GroupResponse], status_code=status.HTTP_200_OK)
async def list_groups(
    status_filter: str | None = Query(None, alias="status"),
    current_coordinator: Student = Depends(get_current_coordinator),
    db: Session = Depends(get_db),
) -> list[GroupResponse]:
    query = db.query(ProjectGroup).options(joinedload(ProjectGroup.students))
    if status_filter:
        query = query.filter(ProjectGroup.status == status_filter)

    groups = query.all()

    response_list = []
    for g in groups:
        member_emails = []
        partners = []
        for s in g.students:
            if s.email:
                member_emails.append(s.email)
            partners.append(
                PartnerInfo(
                    id=s.id,
                    name=s.name,
                    email=s.email,
                    github_username=s.github_username,
                    invite_status=s.invite_status,
                )
            )
        
        response_list.append(
            GroupResponse(
                id=g.id,
                group_no=g.group_no,
                group_name=g.group_name,
                team_name=g.team_name,
                repo_name=g.repo_name,
                github_repo_url=g.github_repo_url,
                status=g.status,
                member_emails=member_emails,
                partners=partners,
            )
        )

    return response_list


@router.get("/groups/{group_id}/details", response_model=GroupDeepDiveResponse, status_code=status.HTTP_200_OK)
async def get_group_details(
    group_id: int,
    current_coordinator: Student = Depends(get_current_coordinator),
    db: Session = Depends(get_db),
) -> GroupDeepDiveResponse:
    group = (
        db.query(ProjectGroup)
        .options(
            joinedload(ProjectGroup.students),
            joinedload(ProjectGroup.comments),
        )
        .filter(ProjectGroup.id == group_id)
        .first()
    )
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project group with id {group_id} not found.",
        )

    repo = db.query(GroupRepository).filter(GroupRepository.group_id == group.id).first()
    repo_schema = (
        GroupRepositorySchema(
            id=repo.id,
            group_id=repo.group_id,
            repo_name=repo.repo_name,
            status=repo.status,
        )
        if repo
        else None
    )

    student_ids = [s.id for s in group.students]
    invites = (
        db.query(StudentGithubInvite)
        .filter(StudentGithubInvite.student_id.in_(student_ids))
        .all()
        if student_ids
        else []
    )
    invite_schemas = [
        StudentGithubInviteSchema(
            id=inv.id,
            student_id=inv.student_id,
            github_username=inv.github_username,
            invite_status=inv.invite_status,
        )
        for inv in invites
    ]

    member_schemas = [
        StudentInfo(
            id=s.id,
            name=s.name,
            email=s.email,
            reg_id=s.reg_id,
            is_verified=s.is_verified,
            github_username=s.github_username,
        )
        for s in group.students
    ]

    comment_schemas = [
        CommentSchema(
            id=c.id,
            content=c.content,
            author_id=c.author_id,
            created_at=c.created_at,
        )
        for c in group.comments
    ]

    member_emails = [s.email for s in group.students if s.email]
    group_info = GroupResponse(
        id=group.id,
        group_no=group.group_no,
        group_name=group.group_name,
        team_name=group.team_name,
        repo_name=group.repo_name,
        github_repo_url=group.github_repo_url,
        status=group.status,
        member_emails=member_emails,
    )

    return GroupDeepDiveResponse(
        group_info=group_info,
        members=member_schemas,
        comments=comment_schemas,
        repository_info=repo_schema,
        invite_statuses=invite_schemas,
    )


@router.patch("/groups/{group_id}/status", response_model=GroupStatusUpdateResponse, status_code=status.HTTP_200_OK)
async def update_group_status(
    group_id: int,
    update_data: GroupStatusUpdate,
    background_tasks: BackgroundTasks,
    current_coordinator: Student = Depends(get_current_coordinator),
    db: Session = Depends(get_db),
) -> GroupStatusUpdateResponse:
    group = db.query(ProjectGroup).filter(ProjectGroup.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project group with id {group_id} not found.",
        )

    group.status = update_data.status

    feedback_text: str | None = None
    if update_data.feedback and update_data.feedback.strip():
        feedback_text = update_data.feedback.strip()
        comment = SystemComment(
            group_id=group.id,
            author_id=current_coordinator.id,
            content=feedback_text,
        )
        db.add(comment)

    db.commit()
    db.refresh(group)

    member_emails = [s.email for s in group.students if s.email]

    # Use group_name for the email subject line
    display_name = group.group_name or f"Group #{group.id}"
    background_tasks.add_task(
        send_group_status_email,
        member_emails,
        display_name,
        update_data.status,
        update_data.feedback,
    )

    return GroupStatusUpdateResponse(
        id=group.id,
        group_name=group.group_name,
        team_name=group.team_name,
        status=group.status,
        member_emails=member_emails,
        feedback=feedback_text,
    )
