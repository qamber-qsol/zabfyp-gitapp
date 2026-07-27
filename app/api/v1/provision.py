from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
import time

from app.database import get_db
from app.models.group import ProjectGroup
from app.services.github_client import github_service

router = APIRouter()

def process_bulk_provisioning(db: Session):
    """
    Background worker that iterates through pending groups
    and provisions them on GitHub.
    """
    # Fetch all groups that haven't been provisioned yet
    pending_groups = db.query(ProjectGroup).filter(ProjectGroup.status == "pending").all()
    
    print(f"Starting provisioning for {len(pending_groups)} groups...")

    for group in pending_groups:
        print(f"Provisioning: {group.repo_name}...")
        
        # Extract the @szabist.pk emails for this specific group
        emails = [student.email for student in group.students if student.email]
        
        # Trigger the GitHub API Service
        results = github_service.provision_group(
            repo_name=group.repo_name,
            team_name=group.team_name,
            student_emails=emails
        )
        
        # If successfully created, update database state
        if results.get("repo_created") and results.get("team_created"):
            group.status = "provisioned"
            db.commit()
            print(f"✅ Success: {group.repo_name}")
        else:
            print(f"❌ Failed: {group.repo_name} - Errors: {results.get('errors')}")
        
        # CRITICAL: 2-second sleep to prevent GitHub API rate limiting
        time.sleep(2)

    print("🏁 Bulk provisioning complete!")

@router.post("/bulk")
def trigger_bulk_provisioning(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Endpoint to trigger the background provisioning task.
    """
    background_tasks.add_task(process_bulk_provisioning, db)
    return {
        "status": "Accepted", 
        "message": "Bulk provisioning started in the background. Check your terminal for live progress."
    }