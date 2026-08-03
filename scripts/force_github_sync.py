import os
import sys

# Add project root to path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.group import ProjectGroup
from app.services.github_client import github_service
from app.core.config import settings

def run_force_sync():
    db = SessionLocal()
    print("--- STARTING BRUTE FORCE GITHUB PROVISIONING ---")
    
    # Fetch ALL groups without a GitHub repo, completely ignoring the 'pending' status blocker
    groups = db.query(ProjectGroup).filter(ProjectGroup.github_repo_url.is_(None)).all()
    print(f"Found {len(groups)} groups needing GitHub provisioning in the database.")
    
    for group in groups:
        repo_name = group.repo_name or f"fyp-{group.group_no or group.id}-{group.group_name.replace(' ', '-')}"
        team_name = group.team_name or f"Team-{group.group_no or group.id}"
        student_emails = [s.email for s in group.students if s.email]
        
        print(f"\n[Processing] Group ID: {group.id} | Team: {team_name} | Repo: {repo_name}")
        print(f"  -> Students to invite: {student_emails}")
        
        try:
            # Physically creates team, repo, and adds users on GitHub Live Organization
            res = github_service.provision_group(
                repo_name=repo_name,
                team_name=team_name,
                student_emails=student_emails
            )
            
            if res.get("repo_created"):
                repo_url = f"https://github.com/{settings.GITHUB_ORG_NAME}/{repo_name}"
                group.github_repo_url = repo_url
                db.commit()
                print(f"  [SUCCESS] Repo created: {repo_url}")
                print(f"  [SUCCESS] Invites sent: {res.get('invites_sent', 0)}")
            else:
                print(f"  [FAILED] GitHub API Error: {res.get('errors')}")
        except Exception as e:
            db.rollback()
            print(f"  [CRASH] Exception occurred: {str(e)}")
    
    print("\n--- PROVISIONING COMPLETE ---")
    db.close()

if __name__ == "__main__":
    run_force_sync()
