import hashlib
import hmac

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.group import ProjectGroup
from app.models.webhook import PushEvent

router = APIRouter()

@router.post("/github")
async def handle_github_webhook(
    request: Request,
    x_hub_signature_256: str = Header(None),
    x_github_event: str = Header(None),
    db: Session = Depends(get_db)
):
    try:
        # 1. Cryptographic Security Check
        if not x_hub_signature_256:
            raise HTTPException(status_code=401, detail="Missing signature header")
        
        # Read raw bytes to calculate HMAC
        payload_body = await request.body()
        
        # Calculate expected signature using your WEBHOOK_SECRET
        hash_object = hmac.new(
            settings.WEBHOOK_SECRET.encode('utf-8'),
            msg=payload_body,
            digestmod=hashlib.sha256
        )
        expected_signature = "sha256=" + hash_object.hexdigest()
        
        if not hmac.compare_digest(expected_signature, x_hub_signature_256):
            raise HTTPException(status_code=401, detail="Invalid webhook signature")

        # 2. Process the Push Event
        if x_github_event == "push":
            data = await request.json()
            
            # GitHub sends "after" as the ID of the newest commit
            commit_hash = data.get("after")
            repo_name = data.get("repository", {}).get("name")
            
            # Ignore empty pushes or branch deletions
            if commit_hash == "0000000000000000000000000000000000000000":
                return {"status": "ignored", "reason": "branch deleted"}

            # Find which group this repo belongs to
            group = db.query(ProjectGroup).filter_by(repo_name=repo_name).first()
            
            if group:
                # Check if this exact commit was already logged
                existing = db.query(PushEvent).filter_by(commit_hash=commit_hash).first()
                if not existing:
                    # Log it for HoD oversight and your approval
                    head_commit = data.get("head_commit", {})
                    timestamp = head_commit.get("timestamp", "unknown")
                    
                    new_push = PushEvent(
                        group_id=group.id,
                        commit_hash=commit_hash,
                        timestamp=timestamp,
                        approval_status="pending"
                    )
                    db.add(new_push)
                    db.commit()
                    print(f"📥 New Push Detected! Repo: {repo_name} | Status: Pending Approval")
                    
        return {"status": "success", "message": "Webhook processed successfully"}
    except Exception as e:
        print(f"❌ Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")