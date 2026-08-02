from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_student
from app.core.database import get_db
from app.models.group import ProjectGroup
from app.models.student import Student
from app.schemas.group import GroupCreate, GroupResponse

router = APIRouter(tags=["Student Groups"])


@router.post("/", response_model=GroupResponse, status_code=status.HTTP_201_CREATED)
async def create_group(
    group_in: GroupCreate,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
) -> GroupResponse:
    if current_student.group_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student is already a member of a project group.",
        )

    # Create new project group
    new_group = ProjectGroup(
        group_name=group_in.name,
        project_title=group_in.project_title,
        description=group_in.description,
        status="pending_approval",
    )
    db.add(new_group)
    db.flush()

    # Assign current student to group
    current_student.group_id = new_group.id

    # Process member_emails
    for email_str in group_in.member_emails:
        clean_email = str(email_str).strip().lower()
        if clean_email == current_student.email.lower():
            continue

        member = db.query(Student).filter(Student.email == clean_email).first()
        if member and member.is_verified and member.group_id is None:
            member.group_id = new_group.id

    db.commit()
    db.refresh(new_group)
    db.refresh(current_student)

    member_emails = [s.email for s in new_group.students if s.email]

    return GroupResponse(
        id=new_group.id,
        name=new_group.group_name or group_in.name,
        project_title=new_group.project_title,
        description=new_group.description,
        status=new_group.status,
        member_emails=member_emails,
    )


@router.get("/me", response_model=GroupResponse, status_code=status.HTTP_200_OK)
async def get_my_group(
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
) -> GroupResponse:
    if current_student.group_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student is not a member of any project group.",
        )

    group = db.query(ProjectGroup).filter(ProjectGroup.id == current_student.group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project group not found.",
        )

    member_emails = [s.email for s in group.students if s.email]

    return GroupResponse(
        id=group.id,
        name=group.group_name or "",
        project_title=group.project_title,
        description=group.description,
        status=group.status,
        member_emails=member_emails,
    )
