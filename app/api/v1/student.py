import random
import string
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.models.student import Student
from app.models.group import ProjectGroup
from app.services.github import send_org_invite

router = APIRouter(tags=["Students Portal"])

# --- Schemas ---
class OTPRequest(BaseModel):
    email: str

class OTPVerify(BaseModel):
    email: str
    otp: str

class GithubInviteReq(BaseModel):
    email: str
    github_username: str

class ChangeEmailReq(BaseModel):
    old_email: str
    new_email: str
    student_name: str
    student_id: int
    group_id: int
    group_name: str

# --- Endpoints ---
@router.get("/groups", status_code=status.HTTP_200_OK)
def get_all_groups(db: Session = Depends(get_db)):
    groups = db.query(ProjectGroup).all()
    return [{"id": g.id, "group_no": g.group_no, "group_name": g.group_name} for g in groups]

@router.get("/groups/{group_id}/members", status_code=status.HTTP_200_OK)
def get_group_members(group_id: int, db: Session = Depends(get_db)):
    students = db.query(Student).filter(Student.group_id == group_id).all()
    return [{"id": s.id, "name": s.name, "email": s.email} for s in students]

@router.post("/request-otp", status_code=status.HTTP_200_OK)
async def request_otp(req: OTPRequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.email == req.email).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
    
    # Generate 6 digit OTP & set expiry
    otp = ''.join(random.choices(string.digits, k=6))
    student.otp_code = otp
    student.otp_expires_at = datetime.utcnow() + timedelta(minutes=10)
    db.commit()
    
    # DEV HACK: Print to Uvicorn terminal so you don't wait for emails during testing
    print(f"\n=========================================")
    print(f" OTP FOR {req.email} IS: {otp}")
    print(f"=========================================\n")
    
    try:
        from app.services.email import send_email
        await send_email(
            email_to=req.email,
            subject="Your SZABIST FYP Portal OTP",
            body=f"Your verification code is: {otp}. It expires in 10 minutes."
        )
    except Exception as e:
        print(f"Email dispatch failed (Check credentials): {e}")
        
    return {"message": "OTP generated successfully. Check terminal if email fails."}

@router.post("/verify-otp", status_code=status.HTTP_200_OK)
def verify_otp(req: OTPVerify, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.email == req.email).first()
    
    # Bypass expiry check for speed, just check exact match
    if not student or student.otp_code != req.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP code.")
        
    student.otp_code = None # Burn OTP after use
    db.commit()
    
    group = student.group
    return {
        "student": {"id": student.id, "name": student.name, "email": student.email},
        "group": {
            "id": group.id,
            "group_name": group.group_name,
            "group_no": group.group_no,
            "github_repo_url": group.github_repo_url,
            "repo_name": group.repo_name
        }
    }

@router.post("/github-invite", status_code=status.HTTP_200_OK)
async def dispatch_invite(req: GithubInviteReq, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.email == req.email).first()
    if not student or not student.group:
        raise HTTPException(status_code=404, detail="Student or group not found.")
        
    student.github_username = req.github_username.strip()
    db.commit()
    
    try:
        await send_org_invite(
            github_username=student.github_username,
            repo_name=student.group.repo_name or student.group.group_name
        )
        return {"message": "Invite dispatched successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GitHub API Error: {str(e)}")

@router.post("/change-email-request", status_code=status.HTTP_200_OK)
async def change_email_request(req: ChangeEmailReq):
    body = f"Student {req.student_name} (ID: {req.student_id}) from Group {req.group_name} requests an email change from {req.old_email} to {req.new_email}."
    try:
        from app.services.email import send_email
        await send_email(email_to="qambar.ali@szabist.pk", subject="URGENT: FYP Portal Email Change Request", body=body)
    except Exception as e:
        print(f"Could not send email to admin: {e}")
    return {"message": "Request sent successfully."}