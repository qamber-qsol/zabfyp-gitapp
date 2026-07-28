from fastapi import APIRouter, Depends, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_current_coordinator
from app.core.database import get_db
from app.models.group import ProjectGroup
from app.models.repository import GroupRepository, StudentGithubInvite
from app.models.student import Student
from app.schemas.coordinator import DashboardMetricsResponse

router = APIRouter(tags=["Coordinator Dashboard"])


@router.get("/overview", response_model=DashboardMetricsResponse, status_code=status.HTTP_200_OK)
async def get_dashboard_overview(
    current_coordinator: Student = Depends(get_current_coordinator),
    db: Session = Depends(get_db),
) -> DashboardMetricsResponse:
    total_students = db.query(func.count(Student.id)).scalar() or 0
    total_groups = db.query(func.count(ProjectGroup.id)).scalar() or 0
    approved_groups = (
        db.query(func.count(ProjectGroup.id)).filter(ProjectGroup.status == "approved").scalar() or 0
    )
    rejected_groups = (
        db.query(func.count(ProjectGroup.id)).filter(ProjectGroup.status == "rejected").scalar() or 0
    )
    pending_github_invites = (
        db.query(func.count(StudentGithubInvite.id)).filter(StudentGithubInvite.invite_status == "pending").scalar()
        or 0
    )
    active_repositories = (
        db.query(func.count(GroupRepository.id)).filter(GroupRepository.status == "active").scalar() or 0
    )

    return DashboardMetricsResponse(
        total_students=total_students,
        total_groups=total_groups,
        approved_groups=approved_groups,
        rejected_groups=rejected_groups,
        pending_github_invites=pending_github_invites,
        active_repositories=active_repositories,
    )
